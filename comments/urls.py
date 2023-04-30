
from django.urls import path
from .views import CommentsView

urlpatterns = [
    path('<int:pk>', CommentsView.as_view(), name='comments'),
]
