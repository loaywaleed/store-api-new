from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

# validator for egyptian phone numbers
PHONE_REGEX = RegexValidator(
    regex=r"^(?:\+20|0)10[0-9]{8}$",
    message=_(
        "Phone number must start with '010' or '+2010' and be 11 digits long (13 with +20). Example: '01012345678' or '+201012345678'"
    ),
)

# validator for email addresses
EMAIL_REGEX = RegexValidator(
    regex=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
    message=_("Enter a valid email address."),
)
