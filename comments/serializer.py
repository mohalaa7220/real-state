from rest_framework import serializers
from rest_framework.validators import ValidationError
from .models import Comments, Testimonials
from users.serializer import UserSerializer


class AddCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comments
        fields = ['text', 'rating']

    def validate_text(self, value):
        if not value:
            raise ValidationError({"message": "Text is required"})
        return value

    def validate_rating(self, value):
        if not value:
            raise ValidationError({"message": "Rating is required"})
        return value

    def create(self, validated_data):
        return super().create(validated_data)


class AllCommentsSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Comments
        fields = ['id', 'text', 'rating', 'user', 'created_at', 'updated_at']


# Testimonials

class TestimonialsSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Testimonials
        fields = '__all__'

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
