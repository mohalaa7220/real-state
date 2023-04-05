from .serializer import (ProductSerializer, AddProductSerializer)
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Product


class Product(generics.ListCreateAPIView):
    serializer_class = AddProductSerializer
    queryset = Product.objects.all()

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Product add successfully"}, status=status.HTTP_201_CREATED)

        else:
            return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        queryset = Product.objects.prefetch_related('images').all()
        serializer = ProductSerializer(queryset, many=True).data
        return Response({"data": serializer}, status=status.HTTP_200_OK)
