from .serializer import (UserSerializer, UserSignupSerializer,
                         PasswordSerializer, ResetPasswordSerializer, VerifyOtpSerializer)
from django.contrib.auth import get_user_model, authenticate, login, logout
from rest_framework import generics, permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth.hashers import make_password
from .email_send import send_otp_via_email


User = get_user_model()


# ------ SignUp ----------
class UserSignupView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSignupSerializer

    def post(self, request):
        data = request.data

        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            response = {
                "message": "User Created Successfully",
                "status": 201
            }
            return Response(data=response, status=status.HTTP_201_CREATED)
        else:
            new_error = {}
            for field_name, field_errors in serializer.errors.items():
                new_error[field_name] = field_errors[0]
            return Response(new_error, status=status.HTTP_400_BAD_REQUEST)


# ----- Login ------
class UserLoginView(ObtainAuthToken):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            token, create = Token.objects.get_or_create(user=user)
            return Response({
                "message": "Login Successfully",
                'data': UserSerializer(user).data,
                "token": token.key
            })
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class UserProfile(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)


# ============================================================================
# Reset Password
# ============================================================================
class PasswordResetView(APIView):

    def post(self, request):
        data = request.data
        serializer = ResetPasswordSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data['email']
            if not User.objects.filter(email=email).exists():
                return Response({"message": 'Invalid Email'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                send_otp_via_email(email)
                return Response({"message": 'code sent'}, status=status.HTTP_200_OK)
        else:
            return Response({"message": 'invalid email'}, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTP(APIView):

    def post(self, request):
        data = request.data
        serializer = VerifyOtpSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data['email']
            otp = serializer.data['otp']

            user = User.objects.filter(email=email)

            if not user.exists():
                return Response({"message": 'invalid email'}, status=status.HTTP_400_BAD_REQUEST)

            if user[0].otp != otp:
                return Response({"message": 'invalid code'}, status=status.HTTP_400_BAD_REQUEST)

            if user[0].otp == otp:
                return Response({"message": "code done", "code": otp}, status=status.HTTP_200_OK)
        else:
            return Response({"message": 'invalid data'}, status=status.HTTP_400_BAD_REQUEST)


class PasswordView(APIView):
    def post(self, request):
        data = request.data

        serializer = PasswordSerializer(data=data)
        if serializer.is_valid():
            password = serializer.data['password']
            email = serializer.data['email']
            user = User.objects.get(email=email)

            user.password = make_password(password)
            user.save()

            return Response({"message": "Password Reset Successfully"}, status=status.HTTP_201_CREATED)
        else:
            new_error = {}
            for field_name, field_errors in serializer.errors.items():
                new_error[field_name] = field_errors[0]
            return Response(new_error, status=status.HTTP_400_BAD_REQUEST)
