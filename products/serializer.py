# serializers.py

from .models import Product
from rest_framework import serializers


# class FeatureSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Feature
#         fields = ['id', 'name']

# class AmenitySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Amenity
#         fields = ['id', 'name']


class AddProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('id', 'name', 'location', 'description', 'beds', 'bathrooms', 'thumbnail_images',
                  'square', 'state', 'price', 'features', 'amenities', 'original_image')

    def create(self, validated_data):
        # features_data = validated_data.pop('features', [])
        # amenities_data = validated_data.pop('amenities', [])
        # product = Product.objects.create(**validated_data)
        # for feature_data in features_data:
        #     feature = Feature.objects.get_or_create(**feature_data)[0]
        #     product.features.add(feature)
        # for amenity_data in amenities_data:
        #     amenity = Amenity.objects.get_or_create(**amenity_data)[0]
        #     product.amenities.add(amenity)

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
