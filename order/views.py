from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import OrderItem
from .serializer import OrderItemSerializer, SimpleOrderItemSerializer, UserOrderItemSerializer
from rest_framework.response import Response
from django.db.models import Q
from django.shortcuts import get_object_or_404


# Create and Return order for user
class OrderItemListCreateView(generics.ListCreateAPIView):
    serializer_class = UserOrderItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return OrderItem.objects.select_related('user').prefetch_related('product').filter(user=self.request.user)

    def post(self, request):
        serializer = OrderItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response({'message': "Order created successfully"}, status=status.HTTP_200_OK)


# Order Details (get , update , delete)
class OrderDetails(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserOrderItemSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return OrderItem.objects.select_related('user').prefetch_related('product').filter(Q(user=self.request.user) & Q(id=pk))


# Remove Product From Order
class RemoveProductFromOrderView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, order_id, product_id):
        order_item = get_object_or_404(OrderItem.objects.select_related(
            'user'), id=order_id, user=request.user)
        product = get_object_or_404(order_item.product.all(), id=product_id)
        order_item.product.remove(product)
        return Response({'message': f"Product with ID {product.name} removed from order"}, status=status.HTTP_200_OK)


class OrderItemAdmin(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = SimpleOrderItemSerializer
    queryset = OrderItem.objects.select_related(
        'user').prefetch_related('product').all()
