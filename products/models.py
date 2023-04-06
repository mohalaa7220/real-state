from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils.text import slugify


class Product(models.Model):
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

    def __str__(self) -> str:
        return self.name


class Amenities(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


class Features(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name
