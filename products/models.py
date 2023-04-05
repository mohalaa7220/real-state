from django.db import models


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
    features = models.TextField()
    amenities = models.TextField()
    images = models.ManyToManyField('ProductImage')


class ProductImage(models.Model):
    image = models.ImageField(upload_to='product_images')
