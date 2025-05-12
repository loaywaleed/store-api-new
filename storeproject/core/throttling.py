from rest_framework.throttling import AnonRateThrottle, UserRateThrottle


class OTPMinuteThrottle(UserRateThrottle):
    scope = "otp_minute"


class OTPDayThrottle(UserRateThrottle):
    scope = "otp_day"


class PhoneVerificationMinuteThrottle(AnonRateThrottle):
    scope = "phone_verification_minute"


class PhoneVerificationDayThrottle(AnonRateThrottle):
    scope = "phone_verification_day"


class EmailVerificationMinuteThrottle(AnonRateThrottle):
    scope = "email_verification_minute"


class EmailVerificationDayThrottle(AnonRateThrottle):
    scope = "email_verification_day"


