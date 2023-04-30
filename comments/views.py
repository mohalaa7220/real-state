from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from .models import Comments, Product
from .serializer import AddCommentSerializer, AllCommentsSerializer
from django.shortcuts import get_object_or_404
from project.serializer_error import serializer_error


class CommentsView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AllCommentsSerializer
    queryset = Comments.objects.select_related('product', 'user')

    def post(self, request, pk=None):
        data = request.data
        product = get_object_or_404(Product, pk=pk)
        serializer = AddCommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=request.user, product=product)
            return Response({"message": "Comment added successfully"}, status=status.HTTP_201_CREATED)
        else:
            return serializer_error(serializer)
