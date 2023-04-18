from django.db import models
from products.models import Product
from users.models import User


class Order(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    stipe_token = models.CharField(max_length=100)
    paid_amount = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True)
    phone = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    payment = models.CharField(max_length=255)
    user = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.CASCADE)


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, null=True, blank=True, related_name='items')
    product = models.ForeignKey(
        Product, null=True, blank=True, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
