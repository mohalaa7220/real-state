from .models import Product, Amenities, BookProduct
from rest_framework import serializers
from users.serializer import UserSerializer


class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenities
        fields = ['id', 'name']

    def create(self, validated_data):
        return super().create(validated_data)


class AddProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('name', 'location', 'description', 'beds', 'bathrooms', 'thumbnail_images',
                  'square', 'state', 'price', 'amenities', 'original_image', 'added_by')

    # def validate(self, data):
    #     if not data.get('name'):
    #         raise serializers.ValidationError(
    #             {"message": "Name of Product is required."})
    #     if not data.get('quantity'):
    #         raise serializers.ValidationError(
    #             {"message": "quantity is required."})

    #     if not data.get('price'):
    #         raise serializers.ValidationError(
    #             {"message": "price is required."})

    #     if not data.get('description'):
    #         raise serializers.ValidationError(
    #             {"message": "description is required."})

    #     return data

    def create(self, validated_data):
        amenities_data = validated_data.pop('amenities', [])
        product = Product.objects.create(**validated_data)
        for amenity_data in amenities_data:
            amenity = Amenities.objects.get(id=amenity_data.id)
            product.amenities.add(amenity)

        product.save()
        return product


class ProductSerializer(serializers.ModelSerializer):
    thumbnail_images = serializers.SerializerMethodField()
    amenities = AmenitySerializer(many=True)
    qr_code_url = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'name', 'location', 'description', 'beds', 'bathrooms', 'thumbnail_images',
                  'square', 'state', 'price', 'amenities', 'original_image', 'created', 'updated', 'qr_code_url')

    def get_thumbnail_images(self, obj):
        if obj.thumbnail_images:
            return obj.thumbnail_images
        else:
            return []

    def get_qr_code_url(self, obj):
        if obj.qr_code:
            request = self.context.get('request')
            if request is not None:
                return request.build_absolute_uri(obj.qr_code.url)
        return None


class SimpleProductSerializer(serializers.ModelSerializer):
    amenities = AmenitySerializer(many=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'location', 'description', 'square', 'state', 'qr_code',
                  'price', 'amenities', 'original_image', 'created', 'updated')


class SimpleProductOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'location', 'square', 'state')


class UpdateProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('name', 'location', 'description', 'beds', 'bathrooms', 'thumbnail_images',
                  'square', 'state', 'price',  'amenities', 'original_image')

        def update(self, instance, validated_data):
            instance.__dict__.update(**validated_data)
            instance.save()
            return instance


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
                  'product', 'user', 'created', 'updated']
