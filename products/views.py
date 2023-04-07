from .serializer import (
    ProductSerializer, AddProductSerializer, UpdateProductSerializer)
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from .models import Product
from .permissions import IsAdminOrReadOnly
from rest_framework import status


class Products(ListCreateAPIView):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination
    queryset = Product.objects.prefetch_related('features', 'amenities').all()

    def post(self, request, *args, **kwargs):
        serializer = AddProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(added_by=request.user)
        return Response({"message": "Product added successfully"}, status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        paginated_queryset = self.paginate_queryset(queryset)
        serializer = self.get_serializer(paginated_queryset, many=True)
        return self.get_paginated_response(serializer.data)


class UpdateProduct(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = ProductSerializer
    queryset = Product.objects.prefetch_related('features', 'amenities').all()

    def update(self, request, pk=None):
        product = self.get_object()
        serializer = UpdateProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Product Update successfully"}, status=status.HTTP_202_ACCEPTED)
