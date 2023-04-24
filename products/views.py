from .serializer import (
    ProductSerializer, AddProductSerializer, UpdateProductSerializer, BookProductSerializer)
from .cursorPagination import ProductCursorPagination, ProductsPagination
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .models import Product, BookProduct
from .permissions import IsAdminOrReadOnly
from rest_framework import status

from rest_framework.pagination import PageNumberPagination

# ------- Get All Product --------------


class Products(ListCreateAPIView):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = ProductSerializer
    pagination_class = ProductsPagination
    queryset = queryset = Product.objects.prefetch_related(
        'features', 'amenities').all()

    def post(self, request, *args, **kwargs):
        serializer = AddProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(added_by=request.user)
        return Response({"message": "Product added successfully"}, status=status.HTTP_201_CREATED)


# ------- Update - Delete Product --------------
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


# ------- Get All Product For Admin --------------
class ProductsUser(ListCreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = ProductSerializer
    pagination_class = ProductCursorPagination

    def get_queryset(self):
        return Product.objects.prefetch_related('features', 'amenities').filter(added_by=self.request.user)

    def get(self, request):
        queryset = self.get_queryset()
        paginated_queryset = self.paginate_queryset(queryset)
        serializer = self.get_serializer(paginated_queryset, many=True)
        return self.get_paginated_response(serializer.data)


class ProductUserDetails(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = ProductSerializer
    queryset = Product.objects.prefetch_related(
        'features', 'amenities').select_related('added_by')


class BookProductView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookProductSerializer
    queryset = BookProduct.objects.select_related('user', 'product').all()
