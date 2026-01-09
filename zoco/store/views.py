from django.shortcuts import render
from .models import product, category

# Create your views here.
def home(request):
    products = product.objects.all()
    categories = category.objects.all()
    return render(request, 'home.html', {'products': products, 'categories': categories})

def collections(request):
    products = product.objects.all()
    categories = category.objects.all()
    return render(request, 'collections.html', {'products': products, 'categories': categories})

def story(request):
    return render(request, 'story.html')