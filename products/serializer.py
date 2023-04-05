# serializers.py

from .models import Product, ProductImage
from rest_framework import serializers


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('id', 'image')


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'location', 'description', 'num_beds', 'num_bathrooms',
                  'square', 'state', 'price', 'features', 'amenities', 'images')

    def create(self, validated_data):
        images_data = self.context.get('view').request.FILES
        product = Product.objects.create(**validated_data)

        for image_data in images_data.values():
            ProductImage.objects.create(product=product, image=image_data)

        return product
