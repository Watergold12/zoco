from django.db import models
import datetime

# Product's category model
class category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

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
    name = models.CharField(max_length=100)
    price = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    category = models.ForeignKey(category, on_delete=models.CASCADE, default=1)
    description = models.TextField(default='', blank=True, null=True)
    stock_quantity = models.IntegerField()
    image = models.ImageField(upload_to='uploads/products/')

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