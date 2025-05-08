from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Custom user model that extends the default Django user model.
    """

    email = models.EmailField(
        max_length=255,
        unique=True,
        error_messages={
            "unique": _("A user with that email already exists."),
        },
    )
    username = models.CharField(_("username"), max_length=150, null=True, blank=True)
    phone = models.CharField(_("phone"), unique=True, blank=True, null=True)
    otp_code = models.CharField(max_length=4)
    otp_expiry = models.DateTimeField(blank=True, null=True)
