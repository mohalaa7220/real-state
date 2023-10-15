
from django.urls import path
from .views import (CommentsView, CommentDetailsView, TestimonialsView,
                    TestimonialsUser, DetailsTestimonialUser)

urlpatterns = [
    path('comments_product/<int:pk>', CommentsView.as_view(), name='comments'),
    path('comment/<int:pk>', CommentDetailsView.as_view(), name='comment'),

    path('testimonials/', TestimonialsView.as_view(), name='testimonials'),
    path('testimonials_user/', TestimonialsUser.as_view(),
         name='testimonials_user'),
    path('testimonials/<int:pk>', DetailsTestimonialUser.as_view(),
         name='only_testimonials_user'),
]
