from dj_rest_auth.serializers import LoginSerializer
from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework.serializers import ValidationError

# User = get_user_model()


class CustomLoginSerializer(LoginSerializer):
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
        attrs["user"] = user
        return attrs
