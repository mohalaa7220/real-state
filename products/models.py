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
        ('rent', 'Rent'), ('sale', 'Sale')))
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = ArrayField(models.CharField(max_length=100))
    amenities = ArrayField(models.CharField(max_length=100))
    images = models.ManyToManyField('ProductImage', related_name='images')

    def __str__(self) -> str:
        return self.name


class ProductImage(models.Model):
    image = models.ImageField(upload_to='product_images')
