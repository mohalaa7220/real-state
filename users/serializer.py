from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import ValidationError


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'role']
        read_only_fields = ['id', 'role']


# ---------- SignUp user ---------------
class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['name', 'email', 'password', 'role']

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user


# ============================================================================
# Reset Password
# ============================================================================
class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        email_exists = User.objects.filter(email=attrs["email"]).exists()
        if email_exists == False:
            raise ValidationError({"message": "Email does not exist"})
        return super().validate(attrs)


class VerifyOtpSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()


class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=8)
    email = serializers.EmailField()

    def validate(self, attrs):
        email_exists = User.objects.filter(email=attrs["email"]).exists()
        if email_exists == False:
            raise ValidationError({"message": "Email does not exist"})
        return super().validate(attrs)
