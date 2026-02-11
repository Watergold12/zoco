from django.contrib import admin
from .models import Shipping_Address, Order, OrderItem

# Register your models here.
admin.site.register(Shipping_Address)
admin.site.register(Order)
admin.site.register(OrderItem)
