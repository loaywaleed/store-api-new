import random
from datetime import timedelta

from django.core.mail import send_mail
from django.db import transaction
from django.utils import timezone


class OTPMixin:
    """
    Mixin to handle otp management for user verification.
    """

    @transaction.atomic
    def generate_phone_otp(self):
        self.otp = str(random.randint(100000, 999999))
        self.otp_expiration = timezone.now() + timedelta(minutes=5)
        self.save()
        return self.otp

    @transaction.atomic
    def generate_email_otp(self):
        self.otp = str(random.randint(100000, 999999))
        self.otp_expiration = timezone.now() + timedelta(minutes=5)
        self.save()
        return self.otp

    @transaction.atomic
    def verify_phone(self, otp_value):
        if (
            self.otp == otp_value
            and self.otp_expiration
            and self.otp_expiration > timezone.now()
        ):
            self.is_phone_verified = True
            self.otp = None
            self.otp_expiration = None
            self.save()
            return True
        return False

    @transaction.atomic
    def send_phone_otp(self):
        otp = self.generate_phone_otp()
        # sending sms here is not implemented
        print(f"Sending phone OTP: {otp} to {self.phone}")
        return otp

    @transaction.atomic
    def verify_email(self, otp_value):
        if (
            self.otp == otp_value
            and self.otp_expiration
            and self.otp_expiration > timezone.now()
        ):
            self.is_email_verified = True
            self.is_active = True
            self.otp = None
            self.otp_expiration = None
            self.save()
            return True
        return False

    @transaction.atomic
    def send_email_otp(self):
        if not self.email:
            raise ValueError("Email address is required to send OTP")
        otp = self.generate_email_otp()
        send_mail(
            "Your email verification code",
            f"Your verification code is {otp}",
            "no-reply@example.com",
            [self.email],
            fail_silently=False,
        )
        print(f"Sending email OTP: {otp} to {self.email}")
        return otp

    @transaction.atomic
    def reset_otp(self):
        self.otp = None
        self.otp_expiration = None
        self.save()
