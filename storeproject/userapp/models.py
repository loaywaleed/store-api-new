from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from .managers import UserManager


class User(AbstractUser):
    """
    Custom user model that extends the default Django user model.
    #TODO: add validators for email and phone number
    """

    email = models.EmailField(
        _("email"),
        max_length=255,
        unique=True,
        error_messages={
            "unique": _("A user with that email already exists."),
        },
    )
    username = models.CharField(_("username"), max_length=150, null=True, blank=True)
    phone = models.CharField(
        _("phone"), max_length=14, unique=True, blank=True, null=True
    )
    objects = UserManager() 

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["phone"]
