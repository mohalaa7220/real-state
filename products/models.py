from django.db import models
from users.models import User
from django.urls import reverse
import cloudinary.uploader


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
    amenities = models.ManyToManyField('Amenities', related_name='amenities')
    original_image = models.ImageField(
        upload_to='images', null=True, blank=True)
    thumbnail_images = models.JSONField(null=True, blank=True)
    qr_code = models.ImageField(upload_to='qr_codes', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    image_url = models.URLField(blank=True)
    code_url = models.URLField(blank=True)

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if self.original_image:
            response = cloudinary.uploader.upload(self.original_image)
            self.image_url = response['url']

        if self.qr_code:
            response = cloudinary.uploader.upload(self.qr_code)
            self.code_url = response['url']
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.image_url:
            public_id = self.image_url.split('/')[-1].split('.')[0]
            cloudinary.uploader.destroy(public_id)
        super().delete(*args, **kwargs)

    @property
    def qr_code_url(self):
        return (reverse('qr_code', args=[self.pk]))

    class Meta:
        ordering = ('-created',)


class Amenities(models.Model):
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
