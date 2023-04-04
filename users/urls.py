from django.urls import path
from .views import (UserSignupView, UserLoginView, UserProfile,
                    PasswordResetView, PasswordView, VerifyOTP)

urlpatterns = [
    path('signup', UserSignupView.as_view(), name='signup'),
    path('login', UserLoginView.as_view(), name='login'),
    path('profile', UserProfile.as_view(), name='profile'),

    # ============================================================================
    # Reset Password
    # ============================================================================
    path("send_code", PasswordResetView.as_view(), name="send_code"),
    path("verify_otp", VerifyOTP.as_view(), name="verify_oTP"),
    path("password_confirm", PasswordView.as_view(), name="password_confirm"),
]
