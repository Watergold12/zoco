from django.shortcuts import render
from .models import product, category
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

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

def payment(request):
    products = product.objects.all()
    categories = category.objects.all()
    return render(request, 'payment.html', {'products': products, 'categories': categories})

def checkout(request):
    products = product.objects.all()
    categories = category.objects.all()
    return render(request, 'checkout.html', {'products': products, 'categories': categories})

def login_user(request):
    return render(request, 'login.html')

def logout_user(request):
    pass