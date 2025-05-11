import random
from datetime import timedelta

from django.core.mail import send_mail
from django.utils import timezone


class OTPService:

    @staticmethod
    def send_phone_otp(user):
        otp = user.generate_phone_otp()
        print(f"Sending phone OTP: {otp} to {user.phone}")
        # sending sms here is not implemented
        return otp

    @staticmethod
    def send_email_otp(user):
        otp = user.generate_email_otp()
        # sending email
        send_mail(
            "Your email verification code",
            f"Your verification code is {otp}",
            "no-reply@example.com",
            [user.email],
            fail_silently=False,
        )
        print(f"Sending email OTP: {otp} to {user.email}")
        return otp
