from django.db import models
import datetime

from django.forms import ValidationError

# Product's category model
class category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Categories'

# Customer's model
class customer(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=10)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

# Product's model
class product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    price = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    category = models.ForeignKey(category, on_delete=models.CASCADE, default=1)
    description = models.TextField(default='', blank=True, null=True)
    stock_quantity = models.IntegerField()
    image = models.ImageField(upload_to='uploads/products/')
    is_new = models.BooleanField(default=False)
    is_available = models.BooleanField(default=False)
    is_offer = models.BooleanField(default=False)
    offer_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)

    def clean(self):
        # 1. Check if offer is enabled but price is missing
        if self.is_offer and self.offer_price is None:
            raise ValidationError({
                'offer_price': 'You must provide an offer price if "is_offer" is checked.'
            })
        
        # 2. Optional: Clear offer_price if is_offer is False
        if not self.is_offer and self.offer_price is not None:
            # You can either raise an error or just null it out
            self.offer_price = None 

    def save(self, *args, **kwargs):
        self.full_clean() # This ensures clean() is called before saving
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

# Customer Order's model
class order(models.Model):
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    customer = models.ForeignKey(customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    address = models.CharField(max_length=100, default='', blank=False)
    phone = models.CharField(max_length=10, default='', blank=False)
    order_date = models.DateTimeField(default=datetime.datetime.now)
    status = models.BooleanField(default=False)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.product