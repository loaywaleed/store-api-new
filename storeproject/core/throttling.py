from rest_framework.throttling import AnonRateThrottle, UserRateThrottle


class OTPMinuteThrottle(UserRateThrottle):
    scope = "otp_minute"
    rate = "3/minute"


class OTPDayThrottle(UserRateThrottle):
    scope = "otp_day"
    rate = "10/day"


class PhoneVerificationMinuteThrottle(AnonRateThrottle):
    scope = "phone_verification_minute"
    rate = "3/minute"


class PhoneVerificationDayThrottle(AnonRateThrottle):
    scope = "phone_verification_day"
    rate = "20/day"


class EmailVerificationMinuteThrottle(AnonRateThrottle):
    scope = "email_verification_minute"
    rate = "3/minute"


class EmailVerificationDayThrottle(AnonRateThrottle):
    scope = "email_verification_day"
    rate = "20/day"
