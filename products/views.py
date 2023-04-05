from .serializer import (ProductSerializer)
from rest_framework import generics, permissions, status
from .models import Product


class AddProduct(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
