from dj_rest_auth.views import LoginView
from .serializers import CustomLoginSerializer
from storeproject.core.jwt_util import Jwt
from rest_framework.response import Response


class CustomLoginView(LoginView):
    serializer_class = CustomLoginSerializer

    def get_response(self):
        data = Jwt.get_tokens_response(self.user)
        return Response(data)
