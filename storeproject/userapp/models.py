from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import UserManager
from .model_mixins import OTPMixin


class User(AbstractUser, OTPMixin):
    """
    Custom user model that extends the default Django user model.
    #TODO: add validators for email and phone number
    """

    email = models.EmailField(
        _("email"),
        max_length=255,
        unique=True,
        blank=True,
        null=True,
    )
    username = models.CharField(_("username"), max_length=150, null=True, blank=True)
    phone = models.CharField(
        _("phone"),
        max_length=14,
        unique=True,
        blank=False,
        null=False,
    )
    is_active = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)
    is_phone_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, null=True, blank=True)
    otp_expiration = models.DateTimeField(null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["phone"]
