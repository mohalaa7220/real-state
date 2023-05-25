from .serializer import (
    ProductSerializer, AddProductSerializer, UpdateProductSerializer, BookProductSerializer, AmenitySerializer, AddBookProductSerializer)
from .cursorPagination import (ProductCursorPagination, ProductsPagination)
from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import (IsAdminUser, IsAuthenticated)
from .models import (Product, BookProduct, Amenities)
from .permissions import IsAdminOrReadOnly
from rest_framework import status
from django_filters import rest_framework as filters
from .ProductFilter import ProductFilter
from django.shortcuts import get_object_or_404
import qrcode
from django.core.files.base import ContentFile
from io import BytesIO


def generate_qr_code(product):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    data = f"name:{product.name}\n location:{product.location}\n beds:{product.beds} beds, bathrooms: {product.bathrooms} baths square:\n{product.square} sq. ft.\n{product.state}\n${product.price}"
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color='black', back_color='white')
    return img


def save_qr_code(product):
    if product.qr_code is not None:
        img = generate_qr_code(product)
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        product.qr_code.save(f'{product.pk}.png',
                             ContentFile(buffer.getvalue()))


class Products(ListCreateAPIView):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = ProductSerializer
    pagination_class = ProductsPagination
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = ProductFilter
    queryset = Product.objects.prefetch_related('amenities').all()

    def post(self, request, *args, **kwargs):
        serializer = AddProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(added_by=request.user)
        save_qr_code(serializer.instance)
        return Response({"message": "Product added successfully"}, status=status.HTTP_201_CREATED)


# ------- Update - Delete Product --------------
class UpdateProduct(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = ProductSerializer
    queryset = Product.objects.prefetch_related('amenities').all()

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
        return Product.objects.prefetch_related('amenities').filter(added_by=self.request.user)

    def get(self, request):
        queryset = self.get_queryset()
        paginated_queryset = self.paginate_queryset(queryset)
        serializer = self.get_serializer(paginated_queryset, many=True)
        return self.get_paginated_response(serializer.data)


class ProductUserDetails(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = ProductSerializer
    queryset = Product.objects.prefetch_related(
        'amenities').select_related('added_by')


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
        'amenities').order_by('-created')[:6]


class AmenitiesView(ListCreateAPIView):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = AmenitySerializer
    queryset = Amenities.objects.all()
