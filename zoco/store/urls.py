from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('collections/', views.collections, name='collections'),
    path('story/', views.story, name='story'),
    path('payment/', views.payment, name='payment'),
    path('checkout/', views.checkout, name='checkout'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('product/<int:pk>', views.product_detail, name='product_detail'),
]