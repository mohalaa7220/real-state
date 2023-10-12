from rest_framework.response import Response
from rest_framework import status, views, generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Product, Testimonials
from .serializer import CommentSerializer, TestimonialsSerializer
from django.shortcuts import get_object_or_404
from project.serializer_error import serializer_error
from .models import Comments


# ========= (add , get) comments ==========
class CommentsView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CommentSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response({"message": "Comment added successfully"}, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return Comments.objects.filter(product_id=pk).select_related('product', 'user')


# ========= (update , get,delete) comment ==========
class CommentDetailsView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CommentSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response({"message": "Comment added successfully"}, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        product = get_object_or_404(Product, pk=self.kwargs.get('pk'))
        return product.comments_product.select_related('product', 'user').all()


class TestimonialsView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Testimonials.objects.select_related("user").all()
    serializer_class = TestimonialsSerializer


class TestimonialsUser(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        queryset = user.testimonials_user.all()
        serializer = TestimonialsSerializer(queryset, many=True).data
        return Response(serializer, status=status.HTTP_200_OK)


class DetailsTestimonialUser(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Testimonials.objects.select_related("user").all()
    serializer_class = TestimonialsSerializer
