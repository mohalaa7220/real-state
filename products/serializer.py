# serializers.py

from .models import Product
from rest_framework import serializers


class AddProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('id', 'name', 'location', 'description', 'beds', 'bathrooms', 'thumbnail_images',
                  'square', 'state', 'price', 'features', 'amenities', 'original_image')

    def create(self, validated_data):
        product = Product.objects.create(**validated_data)
        product.save()
        return product


class ProductSerializer(serializers.ModelSerializer):
    thumbnail_images = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'name', 'location', 'description', 'beds', 'bathrooms', 'thumbnail_images',
                  'square', 'state', 'price', 'features', 'amenities', 'original_image')

    def get_thumbnail_images(self, obj):
        if obj.thumbnail_images:
            return obj.thumbnail_images
        else:
            return []
