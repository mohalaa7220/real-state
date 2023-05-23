from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import OrderItem
from .serializer import OrderItemSerializer, SimpleOrderItemSerializer


class OrderItemListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return OrderItem.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OrderItemAdmin(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = SimpleOrderItemSerializer
    queryset = OrderItem.objects.select_related('user', 'product').all()
