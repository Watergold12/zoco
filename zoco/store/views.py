from django.shortcuts import render
from .models import product, category

# Create your views here.
def home(request):
    products = product.objects.all()
    return render(request, 'home.html', {'products': products})

def collections(request):
    return render(request, 'collections.html')

def story(request):
    return render(request, 'story.html')