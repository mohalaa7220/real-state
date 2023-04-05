# serializers.py

from .models import Product, ProductImage
from rest_framework import serializers


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']


class AddProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('id', 'name', 'location', 'description', 'beds', 'bathrooms',
                  'square', 'state', 'price', 'features', 'amenities', 'images')

    def create(self, validated_data):
        images = validated_data.pop('images', [])
        product = Product.objects.create(**validated_data)
        for image_data in images:
            product.images.add(image_data)
        product.save()
        return product


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'location', 'description', 'beds', 'bathrooms',
                  'square', 'state', 'price', 'features', 'amenities', 'images')
