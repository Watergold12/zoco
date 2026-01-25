from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Product, Category
from django.contrib.auth.models import User
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm

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


def size_guide(request):
    return render(request, 'size_guide.html')


def category(request, tpo):
    tpo = tpo.replace("-", " ")
    try:
        category = Category.objects.get(name=tpo)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'products':products, 'category':category})
    except:
        messages.success(request, "That category doesn't exist!!")
        return redirect('home')


def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)

        if user_form.is_valid():
            user_form.save()

            login(request, current_user)
            messages.success(request, "User Profile has been updated!!")
            return redirect('home')
        
        return render(request, 'update_user.html', {'user_form':user_form})
    else:
        messages.success(request, "Please login to update your profile!!")
        return redirect('login')

def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        if request.method == 'POST':
            form = ChangePasswordForm(current_user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Pasword has been updated!!!")
                login(request, current_user)
                return redirect('home')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                return render(request, 'update_password.html', {'form':form})
        else:
            form = ChangePasswordForm(current_user)
            return render(request, 'update_password.html', {'form':form})
    else:
        messages.success(request, "Please login to update your Pasword!!")
        return redirect('login')