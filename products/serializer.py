# serializers.py

from .models import Product, ProductImage
from rest_framework import serializers


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('id', 'name', 'location', 'description', 'beds', 'bathrooms',
                  'square', 'state', 'price', 'features', 'amenities', 'images')

    def create(self, validated_data):
        product = Product.objects.create(**validated_data)
        product.save()
        return product

# def create(self, validated_data):
#         images_data = validated_data.pop('images', [])
#         product = Product.objects.create(**validated_data)
#         for image_data in images_data:
#             image = Image.objects.create(**image_data)
#             product.images.add(image)
#         return product
