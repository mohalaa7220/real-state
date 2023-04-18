from rest_framework import views
from rest_framework.response import Response
from rest_framework import status
from .models import OrderItem
from .serializer import OrderSerializer
from products.models import Product


class checkout(views.APIView):
    serializer_class = OrderSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            order = serializer.save()
            for item in request.data['items']:
                product = Product.objects.get(pk=item['product'])
                OrderItem.objects.create(
                    order=order, product=product, quantity=item['quantity'], price=product.price)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
