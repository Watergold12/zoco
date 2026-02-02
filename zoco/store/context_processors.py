from .models import Product

def products(request):
    return {
        'all_products': Product.objects.all()
    }

