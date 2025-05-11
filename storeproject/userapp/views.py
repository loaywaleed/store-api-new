from dj_rest_auth.views import LoginView
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from storeproject.core.jwt_util import Jwt

from .serializers import (
    CustomLoginSerializer,
    CustomRegisterSerializer,
    VerifyEmailSerializer,
    VerifyPhoneSerializer,
)

User = get_user_model()


class CustomLoginView(LoginView):
    serializer_class = CustomLoginSerializer

    def get_response(self):
        data = Jwt.get_tokens_response(self.user)
        return Response(data)


class RegistrationViewSet(viewsets.GenericViewSet):
    serializer_class = CustomRegisterSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        password = serializer.validated_data.pop("password1")
        serializer.validated_data.pop("password2")

        try:
            user = User.objects.create_user(
                password=password, **serializer.validated_data
            )
        except IntegrityError as e:
            return Response(
                {"detail": "A user with this email or phone already exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user.send_phone_otp()
        return Response(
            {"detail": "User created. OTP sent to phone.", "phone": user.phone},
            status=status.HTTP_201_CREATED,
        )

    @action(detail=False, methods=["post"])
    def verify_phone(self, request):
        serializer = VerifyPhoneSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        user.send_email_otp()
        return Response(
            {"detail": "Phone verified successfully. OTP send to your email."},
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=["post"])
    def verify_email(self, request):
        serializer = VerifyEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            {"detail": "Email verified successfully. you can now log in now."},
        )
