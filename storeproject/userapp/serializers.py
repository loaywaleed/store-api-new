from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer
from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.serializers import ValidationError

User = get_user_model()


class CustomLoginSerializer(LoginSerializer):
    """
    Custom login serializer which overrides the default login serializer (dj_rest_auth).
    allows users to log in using either their email or phone number.
    """

    username = None
    email = None
    identifier = serializers.CharField(required=True, label=_("Email or Phone"))
    password = serializers.CharField(
        style={"input_type": "password"},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        login_identifier = attrs.get("identifier")
        password = attrs.get("password")
        request = self.context.get("request")

        if not login_identifier or not password:
            raise ValidationError("must include identifier")

        user = authenticate(
            request=request, username=login_identifier, password=password
        )
        if not user:
            raise ValidationError("Invalid credentials")
        if not user.is_active:
            raise ValidationError("User account is inactive")
        attrs["user"] = user
        return attrs


class CustomRegisterSerializer(RegisterSerializer):
    """
    Custom registration serializer which overrides the default registration serializer (dj_rest_auth).
    allows users to register using either their email and phone number.
    """

    email = serializers.EmailField(required=True)
    phone = serializers.CharField(required=True, max_length=14)

    def validate(self, attrs):
        phone = attrs.get("phone")
        if User.objects.filter(phone=phone).exists():
            raise ValidationError(_("Phone number already exists"))
        return super().validate(attrs)

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data.update(
            {
                "phone": self.validated_data.get("phone", ""),
            }
        )
        return data


class VerifyPhoneSerializer(serializers.Serializer):
    """
    Serializer for verifying phone number.
    """

    phone = serializers.CharField(required=True, max_length=14)
    otp = serializers.CharField(required=True, max_length=6)

    def validate(self, attrs):
        phone = attrs.get("phone")
        otp = attrs.get("otp")

        user = User.objects.get_user_by_email_or_phone(phone)
        if not user:
            raise ValidationError(_("User with this phone number does not exist"))
        if not user.verify_phone(otp):
            raise ValidationError(_("Invalid OTP"))
        attrs["user"] = user
        return attrs


class VerifyEmailSerializer(serializers.Serializer):
    """
    Serializer for verifying email with OTP.
    """

    email = serializers.EmailField(required=True)
    otp = serializers.CharField(required=True, max_length=6)

    def validate(self, attrs):
        email = attrs.get("email")
        otp = attrs.get("otp")
        user = User.objects.get_user_by_email_or_phone(email)
        if not user:
            raise ValidationError(_("User with this email does not exist"))
        if not user.verify_email(otp):
            raise ValidationError(_("Invalid OTP"))
        attrs["user"] = user
        return attrs


class ResendPhoneOtpSerializer(serializers.Serializer):
    """
    Serializer for resending phone OTP.
    """

    phone = serializers.CharField(required=True, max_length=14)

    def validate(self, attrs):
        phone = attrs.get("phone")

        user = User.objects.get_user_by_email_or_phone(phone)
        if not user:
            raise ValidationError(_("User with this phone number does not exist"))
        if user.is_phone_verified:
            raise ValidationError(_("Phone number already verified"))
        return attrs


class ResendEmailOtpSerializer(serializers.Serializer):
    """
    Serializer for resending email OTP.
    """

    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        email = attrs.get("email")

        user = User.objects.get_user_by_email_or_phone(email)
        if not user:
            raise ValidationError(_("User with this email does not exist"))
        if user.is_email_verified:
            raise ValidationError(_("Email already verified"))
        return attrs

    class InvalidateOtpSerializer(serializers.Serializer):
        """
        Serializer for invalidating OTP.
        identifier: phone or email
        """

        identifier = serializers.CharField(required=True, max_length=14)
        email = serializers.EmailField(required=True)

        def validate(self, attrs):
            identifier = attrs.get("phone")
            user = User.objects.get_user_by_email_or_phone(identifier)
            if not user:
                raise ValidationError(_("User with this identifier does not exist"))
            return attrs
