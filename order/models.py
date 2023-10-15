from django.db import models
from products.models import Product
from users.models import User
from django.db.models.signals import m2m_changed
from django.dispatch import receiver


class OrderItem(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_order_items', blank=True, null=True)
    product = models.ManyToManyField(
        Product,  related_name='product_order_items')
    quantity = models.PositiveIntegerField(default=1)
    address = models.CharField(default=1)
    address = models.CharField(default=1)
    town = models.CharField(default=1)
    country = models.CharField(default=1)
    zip = models.CharField(default=1)
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    order_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        product_names = ', '.join(
            [product.name for product in self.product.all()])
        return f'{product_names} x{self.quantity} => [{self.user}]'


@receiver(m2m_changed, sender=OrderItem.product.through)
def update_total_price(sender, instance, action, **kwargs):
    if action in ('post_add', 'post_remove', 'post_clear', 'post_init'):
        total_price = sum(
            product.price for product in instance.product.all()) * instance.quantity
        instance.total_price = total_price
        instance.save()
