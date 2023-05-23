from rest_framework import serializers
from .models import OrderItem
from users.serializer import UserSerializer
from products.serializer import SimpleProductOrderItemSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        exclude = ('user', )


class SimpleOrderItemSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    product = SimpleProductOrderItemSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = '__all__'
