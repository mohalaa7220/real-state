from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from products.models import Product
from users.models import User


class Comments(models.Model):
    text = models.TextField()
    rating = models.DecimalField(max_digits=2, decimal_places=1, validators=[
                                 MinValueValidator(0), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        User, related_name="comments_user", null=True, on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name="comments_product", null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ('-created_at',)


class Testimonials(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        User, related_name="testimonials_user", null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ('-created_at',)
