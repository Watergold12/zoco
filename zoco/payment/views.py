import json
import hmac
import hashlib

from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import os

import razorpay
import zoco.settings as settings

from cart.cart import Cart
from store.models import Profile

from .forms import ShippingForm
from .models import Order, OrderItem, Shipping_Address

# Initialize Razorpay client
razorpay_client = razorpay.Client(
    auth=(os.getenv('RAZORPAY_KEY_ID'), os.getenv('RAZORPAY_KEY_SECRET'))
)

# Create your views here.
def payment_success(request):
    return render(request, 'payment/payment_success.html', {})


def save_shipping_address_for_user(user, shipping_form):
    shipping_data = shipping_form.cleaned_data
    existing_address = Shipping_Address.objects.filter(user=user).order_by('id').first()

    if existing_address:
        for field, value in shipping_data.items():
            setattr(existing_address, field, value)
        existing_address.save(update_fields=list(shipping_data.keys()))
        return existing_address

    return Shipping_Address.objects.create(user=user, **shipping_data)


def build_shipping_snapshot(shipping_address):
    return (
        f"{shipping_address.shipping_address1}, "
        f"{shipping_address.shipping_address2}, "
        f"{shipping_address.shipping_city}, "
        f"{shipping_address.shipping_state} - {shipping_address.shipping_zipcode}"
    )


def create_order_from_cart(user, cart, shipping_address):
    cart_items = cart.get_cart_items()
    if not cart_items:
        raise ValueError("Your cart is empty.")

    amount_paid = cart.get_total()

    with transaction.atomic():
        order = Order.objects.create(
            user=user,
            shipping_address_ref=shipping_address,
            full_name=shipping_address.shipping_full_name,
            email=shipping_address.shipping_email,
            shipping_address=build_shipping_snapshot(shipping_address),
            amount_paid=amount_paid,
        )

        order_items = []
        for item in cart_items:
            product = item['product']
            item_price = product.offer_price if product.is_offer and product.offer_price is not None else product.price
            order_items.append(
                OrderItem(
                    order=order,
                    product=product,
                    user=user,
                    quantity=item['quantity'],
                    price=item_price,
                )
            )

        OrderItem.objects.bulk_create(order_items)

    return order


@require_POST
def place_order(request):
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'

    if not request.user.is_authenticated:
        if is_ajax:
            return JsonResponse({'success': False, 'message': 'Authentication required.'}, status=401)
        messages.warning(request, "Please login to proceed!")
        return redirect('login')

    shipping_address = Shipping_Address.objects.filter(user=request.user).order_by('id').first()
    if not shipping_address:
        message = "Please save your delivery address before placing an order."
        if is_ajax:
            return JsonResponse({'success': False, 'message': message}, status=400)
        messages.warning(request, message)
        return redirect('payment:checkout')

    cart = Cart(request)
    try:
        order = create_order_from_cart(request.user, cart, shipping_address)
    except ValueError as exc:
        if is_ajax:
            return JsonResponse({'success': False, 'message': str(exc)}, status=400)
        messages.warning(request, str(exc))
        return redirect('payment:checkout')

    # Clear session cart once order rows are persisted.
    request.session['session_key'] = {}
    request.session.modified = True
    Profile.objects.filter(user=request.user).update(old_cart=json.dumps({}))

    if is_ajax:
        return JsonResponse({
            'success': True,
            'order_id': order.id,
            'redirect_url': reverse('payment:payment_success'),
        })

    messages.success(request, f"Order #{order.id} has been created.")
    return redirect('payment:payment_success')


def checkout(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Please login to proceed!")
        return redirect('login')

    shipping_user = Shipping_Address.objects.filter(user=request.user).order_by('id').first()

    if request.method == 'POST':
        shipping_form = ShippingForm(request.POST)
        if shipping_form.is_valid():
            save_shipping_address_for_user(request.user, shipping_form)
            messages.success(request, "Your address has been saved.")
            return redirect('payment:checkout')
        messages.error(request, "Please correct the errors below.")
    else:
        shipping_form = ShippingForm(instance=shipping_user)

    cart = Cart(request)
    cart_items = cart.get_cart_items()
    total = cart.get_total()

    context = {
        'shipping_form': shipping_form,
        'cart_items': cart_items,
        'cart': cart,
        'total': total,
    }

    return render(request, 'payment/checkout.html', context)


@require_POST
def create_razorpay_order(request):
    """
    API endpoint to create a Razorpay order.
    Called by frontend before opening Razorpay checkout modal.
    """
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'message': 'Authentication required.'}, status=401)

    try:
        cart = Cart(request)
        total_amount = cart.get_total()

        # Convert to paise (Razorpay uses paise, 1 INR = 100 paise)
        amount_in_paise = int(float(total_amount) * 100)

        # Minimum amount check
        if amount_in_paise < 100:
            return JsonResponse({
                'success': False,
                'message': 'Minimum order amount is ₹1'
            }, status=400)

        print("KEY:", settings.RAZORPAY_KEY_ID)
        
        # Create Razorpay order
        razorpay_order = razorpay_client.order.create({
            'amount': amount_in_paise,
            'currency': 'INR',
            'receipt': f'order_{request.user.id}_{request.session.session_key}',
        })
        
        print("ORDER:", razorpay_order)

        return JsonResponse({
            'success': True,
            'razorpay_order_id': razorpay_order['id'],
            'razorpay_key_id': os.getenv('RAZORPAY_KEY_ID'),
            'amount': amount_in_paise,
            'user_email': request.user.email,
            'user_name': request.user.get_full_name() or request.user.username,
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error creating order: {str(e)}'
        }, status=500)


@csrf_exempt
@require_POST
def verify_razorpay_payment(request):
    """
    API endpoint to verify Razorpay payment signature.
    Called after user completes payment on Razorpay modal.
    """
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'message': 'Authentication required.'}, status=401)

    try:
        data = json.loads(request.body)
        razorpay_payment_id = data.get('razorpay_payment_id')
        razorpay_order_id = data.get('razorpay_order_id')
        razorpay_signature = data.get('razorpay_signature')

        # Validate required fields
        if not all([razorpay_payment_id, razorpay_order_id, razorpay_signature]):
            return JsonResponse({
                'success': False,
                'message': 'Missing payment details'
            }, status=400)

        # Verify signature using HMAC-SHA256
        key_secret = os.getenv('RAZORPAY_KEY_SECRET')
        generated_signature = hmac.new(
            key_secret.encode(),
            f'{razorpay_order_id}|{razorpay_payment_id}'.encode(),
            hashlib.sha256
        ).hexdigest()

        if generated_signature != razorpay_signature:
            return JsonResponse({
                'success': False,
                'message': 'Payment signature verification failed'
            }, status=400)

        # Signature verified, now create the order
        shipping_address = Shipping_Address.objects.filter(user=request.user).order_by('id').first()
        if not shipping_address:
            return JsonResponse({
                'success': False,
                'message': 'Shipping address not found'
            }, status=400)

        cart = Cart(request)
        try:
            order = create_order_from_cart(request.user, cart, shipping_address)
        except ValueError as exc:
            return JsonResponse({
                'success': False,
                'message': str(exc)
            }, status=400)

        # Clear cart
        request.session['session_key'] = {}
        request.session.modified = True
        Profile.objects.filter(user=request.user).update(old_cart=json.dumps({}))

        return JsonResponse({
            'success': True,
            'message': 'Payment verified successfully',
            'order_id': order.id,
            'redirect_url': reverse('payment:payment_success'),
        })

    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Invalid request format'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error verifying payment: {str(e)}'
        }, status=500)
