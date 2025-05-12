from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from storeproject.core.validators import EMAIL_REGEX, PHONE_REGEX

from .managers import UserManager
from .model_mixins import OTPMixin


class User(AbstractUser, OTPMixin):
    """
    Custom user model that extends the default Django user model.
    """

    email = models.EmailField(
        _("email"),
        max_length=255,
        unique=True,
        blank=True,
        null=True,
        validators=[EMAIL_REGEX],
    )
    username = models.CharField(_("username"), max_length=150, null=True, blank=True)
    phone = models.CharField(
        _("phone"),
        max_length=13,
        unique=True,
        blank=False,
        null=False,
        validators=[PHONE_REGEX],
        help_text=_(
            "Egyptian phone number in format: '01012345678' or '+201012345678'"
        ),
    )
    is_active = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)
    is_phone_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, null=True, blank=True)
    otp_expiration = models.DateTimeField(null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["phone"]
