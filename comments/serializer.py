from rest_framework import serializers
from rest_framework.validators import ValidationError
from .models import Comments


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
