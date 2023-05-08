from typing import Any, Iterable, Optional
from django.db import models
from django.contrib.postgres.fields import ArrayField
from users.models import User


class Product(models.Model):
    added_by = models.ForeignKey(
        User, related_name="user_products", null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.TextField()
    beds = models.IntegerField()
    bathrooms = models.IntegerField()
    square = models.DecimalField(max_digits=8, decimal_places=2)
    state = models.CharField(max_length=10, choices=(
        ('rent', 'rent'), ('sale', 'sale')))
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.ManyToManyField('Features', related_name='features')
    amenities = models.ManyToManyField('Amenities', related_name='amenities')
    original_image = models.ImageField(
        upload_to='images', null=True, blank=True)
    thumbnail_images = models.JSONField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ('-created',)


class Amenities(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        return super().save(*args, **kwargs)


class Features(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        return super().save(*args, **kwargs)


class BookProduct(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    user = models.ForeignKey(
        User, blank=True, null=True, related_name='book_user', on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, blank=True, null=True, related_name='book_product', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.message

    class Meta:
        ordering = ('-created',)
