from django.contrib import admin
from .models import Product, ProductImage

admin.site.register(ProductImage)
admin.site.register(Product)
