from django.shortcuts import render, get_object_or_404
from .cart import Cart
from store.models import Product
from django.http import JsonResponse

# Create your views here.
def cart_summary(request):
    return render(request, "cart.html", {})

def cart_add(request):
    # Get the cart
    cart = Cart(request)
    # test for POST
    if request.POST.get('action') == 'post':
        # get stuff
        product_id = int(request.POST.get('product_id'))
        
        # lookup in DB
        product = get_object_or_404(Product, id=product_id)
        
        # Save to session
        cart.add(product=product)

        # Get cart qty
        cart_quantity = cart.__len__()
        # response = JsonResponse({'Product Name' : product.name})
        response = JsonResponse({'qty' : cart_quantity})
        return response

def cart_delete():
    pass

def cart_update():
    pass