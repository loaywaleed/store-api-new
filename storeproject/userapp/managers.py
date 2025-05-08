from django.contrib.auth.models import BaseUserManager
from django.db import models


class UserManager(BaseUserManager):

    def create_user(self, email, phone, password=None, **extra_fields):
        if not email and not phone:
            raise ValueError("Users need to provide an email or phone")
        if email:
            email = self.normalize_email(email)
        else:
            email = None
        user = self.model(email=email, phone=phone, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, phone, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if not email:
            raise ValueError("Superuser must have an email")
        if not phone:
            raise ValueError("Superuser must have a phone number")
        return self.create_user(email, phone, password, **extra_fields)

    def get_user_by_email_or_phone(self, identifier):
        return self.filter(
            models.Q(email=identifier) | models.Q(phone=identifier)
        ).first()
