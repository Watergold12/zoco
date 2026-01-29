from django.shortcuts import render, get_object_or_404
from .cart import Cart
from store.models import Product
from django.http import JsonResponse
from django.contrib import messages

# Create your views here.
def cart_summary(request):
    cart = Cart(request)
    cart_items = cart.get_cart_items()
    return render(request, "cart.html", {"cart_items":cart_items})

def cart_add(request):
    # Get the cart
    cart = Cart(request)
    # test for POST
    if request.POST.get('action') == 'post':
        # get stuff
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        product_size = request.POST.get('product_size')
        
        # lookup in DB
        product = get_object_or_404(Product, id=product_id)
        
        # Save to session
        cart.add(product=product, quantity=product_qty, size=product_size)

        # Get cart qty
        cart_quantity = cart.__len__()

        # response = JsonResponse({'Product Name' : product.name})
        response = JsonResponse({'qty' : cart_quantity})
        return response

def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        # get stuff - this is now the compound key 'product_id_size'
        product_key = request.POST.get('product_id')

        cart.delete(product_key=product_key)
        response = JsonResponse({'product':product_key})

        messages.success(request, ("Product deleted!"))
        return response

def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        # get stuff - this is now the compound key 'product_id_size'
        product_key = request.POST.get('product_id')
        product_qty = int(request.POST.get('product_qty'))

        cart.update(product_key=product_key, quantity=product_qty)

        response = JsonResponse({'qty': product_qty})
        messages.success(request, ("Product updated!"))
        return response
        # return redirect('cart_summary')