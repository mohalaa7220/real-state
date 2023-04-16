from .models import Product, Amenities, Features, BookProduct
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
        fields = ('name', 'location', 'description', 'beds', 'bathrooms', 'thumbnail_images',
                  'square', 'state', 'price', 'features', 'amenities', 'original_image', 'added_by')

    def create(self, validated_data):
        features_data = validated_data.pop('features', [])
        amenities_data = validated_data.pop('amenities', [])
        product = Product.objects.create(**validated_data)
        for feature_data in features_data:
            feature = Features.objects.get(id=feature_data.id)
            product.features.add(feature)
        for amenity_data in amenities_data:
            amenity = Amenities.objects.get(id=amenity_data.id)
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
                  'square', 'state', 'price', 'features', 'amenities', 'original_image', 'created', 'updated')

    def get_thumbnail_images(self, obj):
        if obj.thumbnail_images:
            return obj.thumbnail_images
        else:
            return []


class UpdateProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('name', 'location', 'description', 'beds', 'bathrooms', 'thumbnail_images',
                  'square', 'state', 'price', 'features', 'amenities', 'original_image')

        def update(self, instance, validated_data):
            instance.__dict__.update(**validated_data)
            instance.save()
            return instance


class BookProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookProduct
        fields = ['id', 'name', 'email', 'product', 'user']

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        instance.__dict__.update(**validated_data)
        instance.save()
        return instance
