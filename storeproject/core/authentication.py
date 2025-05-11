from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

UserModel = get_user_model()


class CustomEmailorPhoneAuthentication(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Authenticates identifier (could be email or phone number)
        """
        user = None
        if username:
            user = UserModel.objects.get_user_by_email_or_phone(username)

        if user and user.check_password(password):
            return user
        return None
