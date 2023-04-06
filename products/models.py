from django.db import models
from django.contrib.postgres.fields import ArrayField


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
    features = ArrayField(models.CharField(max_length=100))
    amenities = ArrayField(models.CharField(max_length=100))
    original_image = models.ImageField(
        upload_to='images', null=True, blank=True)
    thumbnail_images = models.JSONField(null=True, blank=True)

    def __str__(self) -> str:
        return self.name
