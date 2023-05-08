from .serializer import (
    ProductSerializer, AddProductSerializer, UpdateProductSerializer, BookProductSerializer, AmenitySerializer, AddBookProductSerializer, FeatureSerializer)
from .cursorPagination import ProductCursorPagination, ProductsPagination
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .models import (Product, BookProduct, Amenities, Features)
from .permissions import IsAdminOrReadOnly
from rest_framework import status
from django_filters import rest_framework as filters
from .ProductFilter import ProductFilter
from django.shortcuts import get_object_or_404

# ------- Get All Product --------------


class Products(ListCreateAPIView):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = ProductSerializer
    pagination_class = ProductsPagination
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = ProductFilter
    queryset = queryset = Product.objects.prefetch_related(
        'features', 'amenities').all()

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

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


class AddBookProductView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk=None):
        data = request.data
        user = request.user
        product = get_object_or_404(Product, pk=pk)
        serializer = AddBookProductSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user, product=product)
        return Response({"message": "Your Book Product , we will contact you as soon as possible"})


class BookProducts(ListCreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = BookProductSerializer
    queryset = BookProduct.objects.select_related('user', 'product').all()


class LastProductView(ListCreateAPIView):
    serializer_class = ProductSerializer
    queryset = queryset = Product.objects.prefetch_related(
        'features', 'amenities').order_by('-created')[:6]


class AmenitiesView(ListCreateAPIView):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = AmenitySerializer
    queryset = Amenities.objects.all()


class FeaturesView(ListCreateAPIView):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = FeatureSerializer
    queryset = Features.objects.all()
