from .serializer import (ProductSerializer, AddProductSerializer)
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from .models import Product
from rest_framework import status


class Products(ListCreateAPIView):
    serializer_class = AddProductSerializer
    pagination_class = PageNumberPagination

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Product added successfully"}, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        return Product.objects.prefetch_related('features', "amenities").all()

    def get(self, request):
        paginated_queryset = self.paginate_queryset(self.get_queryset())
        serializer = ProductSerializer(paginated_queryset, many=True)
        return self.get_paginated_response(serializer.data)
