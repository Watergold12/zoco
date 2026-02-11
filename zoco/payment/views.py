from django.shortcuts import render
from .forms import ShippingForm
from .models import Shipping_Address
from django.contrib import messages
from django.shortcuts import render, redirect

# Create your views here.
def payment_success(request):
    return render(request, 'payment/payment_success.html', {})

def checkout(request):
    if request.user.is_authenticated:
        # Get existing shipping address for this user
        shipping_user = Shipping_Address.objects.filter(user=request.user).first()
        
        if request.method == 'POST':
            # Handle form submission
            Shipping_form = ShippingForm(request.POST, instance=shipping_user)
            if Shipping_form.is_valid():
                # Save the form but don't commit yet
                shipping_address = Shipping_form.save(commit=False)
                # Associate with the current user
                shipping_address.user = request.user
                # Now save to database
                shipping_address.save()
                messages.success(request, "Your Address has been saved!")
                # Redirect to payment page instead of checkout
                return redirect('payment')
            else:
                # Form has errors, show them
                messages.error(request, "Please correct the errors below.")
        else:
            # GET request - show the form
            Shipping_form = ShippingForm(instance=shipping_user)
        
        # Use the Cart class to get cart items properly
        from cart.cart import Cart
        cart = Cart(request)
        cart_items = cart.get_cart_items()
        total = cart.get_total()
        
        context = {
            'shipping_form': Shipping_form,
            'cart_items': cart_items,
            'cart': cart,
            'total': total
        }
        
        return render(request, 'payment/checkout.html', context)
    else:
        messages.warning(request, "Please login to proceed!")
        return redirect('login')