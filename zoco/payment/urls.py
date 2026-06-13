from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
    path('payment_success/', views.payment_success, name='payment_success'),
    path('checkout/', views.checkout, name='checkout'),
    path('place-order/', views.place_order, name='place_order'),
    path('api/create-order/', views.create_razorpay_order, name='create_order'),
    path('api/verify-payment/', views.verify_razorpay_payment, name='verify_payment'),
]
