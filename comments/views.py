from rest_framework.response import Response
from rest_framework import status, generics, views
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Comments, Product
from .serializer import AddCommentSerializer, AllCommentsSerializer
from django.shortcuts import get_object_or_404
from project.serializer_error import serializer_error


class CommentsView(views.APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = AllCommentsSerializer

    def post(self, request, pk=None):
        data = request.data
        product = get_object_or_404(Product, pk=pk)
        serializer = AddCommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=request.user, product=product)
            return Response({"message": "Comment added successfully"}, status=status.HTTP_201_CREATED)
        else:
            return serializer_error(serializer)

    def get(self, request,  pk=None):
        product = get_object_or_404(Product, pk=pk)
        comments = product.comments_product.select_related(
            'product', 'user').all()
        serializer = self.serializer_class(comments, many=True).data
        return Response(serializer, status=status.HTTP_201_CREATED)
