from django.urls import path
from .views import (UserSignupView, UserLoginView, UserProfile)

urlpatterns = [
    path('signup', UserSignupView.as_view(), name='signup'),
    path('login', UserLoginView.as_view(), name='login'),
    path('profile', UserProfile.as_view(), name='profile'),
]
