from rest_framework import serializers
from rest_framework.validators import ValidationError
from .models import Comments, Testimonials
from users.serializer import UserSerializer
from products.models import Product


class CommentSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.prefetch_related('amenities'), write_only=True)

    class Meta:
        model = Comments
        fields = ['id', 'text', 'rating', 'product',
                  'user', 'created_at', 'updated_at']

    def validate(self, attrs):
        if not attrs.get('text'):
            raise ValidationError({"message": "Text is required"})

        if not attrs.get('rating'):
            raise ValidationError({"message": "Rating is required"})
        return super().validate(attrs)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['user'] = instance.user.name
        return data


# Testimonials
class TestimonialsSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Testimonials
        fields = '__all__'

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
