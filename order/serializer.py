from rest_framework import serializers
from .models import OrderItem, Product
from users.serializer import UserSerializer
from products.serializer import SimpleProductOrderItemSerializer


# Add OrderItem
class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.select_related('added_by'), many=True)

    class Meta:
        model = OrderItem
        exclude = ('user', )

    def create(self, validated_data):
        return super().create(validated_data)


# Return OrderItem
class UserOrderItemSerializer(serializers.ModelSerializer):
    product = SimpleProductOrderItemSerializer(read_only=True, many=True)

    class Meta:
        model = OrderItem
        exclude = ('user', )


# Return All OrderItem for admin
class SimpleOrderItemSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    product = SimpleProductOrderItemSerializer(read_only=True, many=True)

    class Meta:
        model = OrderItem
        fields = '__all__'
