# serializers.py

from .models import Product, Amenities, Features
from rest_framework import serializers


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Features
        fields = ['id', 'name']


class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenities
        fields = ['id', 'name']


class AddProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('id', 'name', 'location', 'description', 'beds', 'bathrooms', 'thumbnail_images',
                  'square', 'state', 'price', 'features', 'amenities', 'original_image')

    def create(self, validated_data):
        features_data = validated_data.pop('features', [])
        amenities_data = validated_data.pop('amenities', [])
        product = Product.objects.create(**validated_data)
        for feature_data in features_data:
            feature = Features.objects.get_or_create(feature_data)[0]
            product.features.add(feature)
        for amenity_data in amenities_data:
            amenity = Amenities.objects.get_or_create(amenity_data)[0]
            product.amenities.add(amenity)

        product.save()
        return product


class ProductSerializer(serializers.ModelSerializer):
    thumbnail_images = serializers.SerializerMethodField()
    features = FeatureSerializer(many=True)
    amenities = AmenitySerializer(many=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'location', 'description', 'beds', 'bathrooms', 'thumbnail_images',
                  'square', 'state', 'price', 'features', 'amenities', 'original_image')

    def get_thumbnail_images(self, obj):
        if obj.thumbnail_images:
            return obj.thumbnail_images
        else:
            return []
