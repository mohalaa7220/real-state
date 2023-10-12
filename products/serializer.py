from .models import Product, Amenities, BookProduct
from rest_framework import serializers
from users.serializer import UserSerializer
from django.db import transaction


class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenities
        fields = ['id', 'name']

    def create(self, validated_data):
        return super().create(validated_data)


# ============== Products Serializer =================
class AddProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('name', 'location', 'description', 'beds', 'bathrooms',
                  'square', 'state', 'price', 'amenities', 'added_by')

    @transaction.atomic
    def create(self, validated_data):
        amenities_data = validated_data.pop('amenities', [])
        product = Product.objects.create(**validated_data)
        product.amenities.set(amenities_data)
        return product


class ProductSerializer(serializers.ModelSerializer):
    amenities = AmenitySerializer(many=True)
    image_url = serializers.URLField(read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'location', 'description', 'beds', 'bathrooms',  'image_url',
                  'square', 'state', 'price', 'amenities', 'created', 'updated',  'code_url')


class SimpleProductSerializer(serializers.ModelSerializer):
    amenities = AmenitySerializer(many=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'location', 'description', 'square', 'state', 'qr_code', 'image_url',
                  'price', 'amenities', 'created', 'updated')


class SimpleProductOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'location', 'square', 'state')


class UpdateProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('name', 'location', 'description', 'beds', 'bathrooms',
                  'square', 'state', 'price',  'amenities')

        def update(self, instance, validated_data):
            instance.__dict__.update(**validated_data)
            instance.save()
            return instance


# ============== Book Product Serializer =================
class AddBookProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookProduct
        fields = ['name', 'email', 'message']

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        instance.__dict__.update(**validated_data)
        instance.save()
        return instance


class BookProductSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    user = UserSerializer()

    class Meta:
        model = BookProduct
        fields = ['id', 'name', 'email', 'message',
                  'product', 'user', 'completed', 'created', 'updated']
