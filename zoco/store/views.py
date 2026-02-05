from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Product, Category, Profile
from django.contrib.auth.models import User
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm
import json
from cart.cart import Cart

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


from cart.cart import Cart

def checkout(request):
    cart = Cart(request)
    cart_items = cart.get_cart_items()
    return render(request, 'checkout.html', {
        'cart_items': cart_items,
    })


def product_detail(request, pk):
    product_obj = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product': product_obj})


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Shopping cart memory
            current_user = Profile.objects.filter(user__id=request.user.id).first()
            # get their cart
            saved_cart = current_user.old_cart if current_user else None
            # xonvert database string to python dictionary
            if saved_cart:
                converted_cart = json.loads(saved_cart)
                # update session cart
                cart = Cart(request)
                # Loop through the cart and add items
                for key, value in converted_cart.items():
                    if isinstance(value, dict):
                        cart.add(
                            product=key,
                            quantity=value.get('quantity') or value.get('qty') or 0,
                            size=value.get('size')
                        )
                    else:
                        cart.add(product=key, quantity=value)
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
            messages.success(request, "Registration successful - Please Fill Out Your Billing Info!!")
            return redirect('update_info')
        else:
            messages.error(request, "Whoops.. There is some issue registering. Please try again!!")
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
    
def update_info(request):
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user__id=request.user.id)
        form = UserInfoForm(request.POST or None, instance=current_user)

        if form.is_valid():
            form.save()
            messages.success(request, "Your Info has been updated!!")
            return redirect('home')
        
        return render(request, 'update_info.html', {'form':form})
    else:
        messages.success(request, "Please login to update your profile!!")
        return redirect('login')
    
def search(request):
    if request.method == "POST":
        searched = request.POST['searched']
        search_results = Product.objects.filter(name__icontains=searched) | \
                         Product.objects.filter(category__name__icontains=searched) | \
                         Product.objects.filter(description__icontains=searched)
                         
        search_results = search_results.distinct()
        
        if not search_results:
            messages.success(request, "That product doesn't exist!!")
            return render(request, 'search.html', {'searched': searched})
        else:
            return render(request, 'search.html', {'searched': searched, 'search_results': search_results})
    else:
        return render(request, 'search.html', {})


