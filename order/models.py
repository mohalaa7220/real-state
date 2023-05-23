from django.db import models
from products.models import Product
from users.models import User


class OrderItem(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_order_items', blank=True, null=True)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='product_order_items', blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)
    address = models.CharField(default=1)
    address = models.CharField(default=1)
    town = models.CharField(default=1)
    country = models.CharField(default=1)
    zip = models.CharField(default=1)
    order_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.product} x{self.quantity} ({self.user.name})'
