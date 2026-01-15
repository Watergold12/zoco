from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Product, Category
from .forms import SignUpForm


def home(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, 'home.html', {
        'products': products,
        'categories': categories
    })


def collections(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, 'collections.html', {
        'products': products,
        'categories': categories
    })


def story(request):
    return render(request, 'story.html')


def payment(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, 'payment.html', {
        'products': products,
        'categories': categories
    })


def checkout(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, 'checkout.html', {
        'products': products,
        'categories': categories
    })


def product_detail(request, pk):
    product_obj = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product': product_obj})


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "Logged in successfully.")
            return redirect('home')

        messages.error(request, "Invalid username or password.")
        return redirect('login')

    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('home')


def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1']
            )
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('home')
    else:
        form = SignUpForm()

    return render(request, 'register.html', {'form': form})
