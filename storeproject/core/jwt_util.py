from rest_framework_simplejwt.tokens import RefreshToken


class Jwt:
    """Wrapper for any jwt utils"""

    @staticmethod
    def get_tokens_response(user):
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        response_data = {
            "acesss": str(access),
            "refresh": str(refresh),
        }
        return response_data
