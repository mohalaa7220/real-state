
from django.urls import path
from .views import (CommentsView, TestimonialsView,
                    TestimonialsUser, DetailsTestimonialUser)

urlpatterns = [
    path('comments/<int:pk>', CommentsView.as_view(), name='comments'),

    path('testimonials/', TestimonialsView.as_view(), name='testimonials'),
    path('testimonials_user/', TestimonialsUser.as_view(),
         name='testimonials_user'),
    path('testimonials/<int:pk>', DetailsTestimonialUser.as_view(),
         name='only_testimonials_user'),
]
