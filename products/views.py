from .serializer import (
    ProductSerializer, AddProductSerializer, UpdateProductSerializer, BookProductSerializer, AmenitySerializer, AddBookProductSerializer)
from .cursorPagination import (ProductsPagination, BooksProductsPagination)
from rest_framework.response import Response
from rest_framework.permissions import (IsAdminUser, IsAuthenticated)
from .models import (Product, BookProduct, Amenities)
from .permissions import IsAdminOrReadOnly
from rest_framework import status, generics
from django_filters import rest_framework as filters
from .ProductFilter import ProductFilter, BookProductFilter
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


# ==========  add product by admin =========
# ==========  get products for all users =========
class Products(generics.ListCreateAPIView):
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


# ==========  get product details for all users =========
# ------- (update - delete) product by admin --------------
class UpdateProduct(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = ProductSerializer
    queryset = Product.objects.prefetch_related('amenities').all()

    def update(self, request, pk=None):
        product = self.get_object()
        serializer = UpdateProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Product Update successfully"}, status=status.HTTP_202_ACCEPTED)

    def delete(self, request, *args, **kwargs):
        self.get_object().delete()
        return Response({"message": "Product deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


# ======== make book for product by user ========
class AddBookProductView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AddBookProductSerializer

    def post(self, request, pk=None):
        user = request.user
        if pk != request.data.get('product'):
            return Response({"message": "product not match"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)
        return Response({"message": "Your Book Product , we will contact you as soon as possible"})


# ======== return books of products (for admin) ========
class BookProducts(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    pagination_class = ProductsPagination
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = BookProductFilter
    serializer_class = BookProductSerializer
    queryset = BookProduct.objects.select_related('user', 'product').all()


# ======== return book details of product (get - update - delete) (for admin) ===========
class BookProductDetails(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = BookProductSerializer
    queryset = BookProduct.objects.select_related('user', 'product').all()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        BookProduct.objects.filter(id=instance.id).update(completed=True)
        return Response({"message": "completed"}, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        self.get_object().delete()
        return Response({"message": "deleted successfully"}, status=status.HTTP_200_OK)


class LastProductView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    queryset = queryset = Product.objects.prefetch_related(
        'amenities').order_by('-created')[:6]


class AmenitiesView(generics.ListCreateAPIView):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = AmenitySerializer
    queryset = Amenities.objects.all()
