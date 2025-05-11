from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import CustomLoginView, RegistrationViewSet

router = DefaultRouter()
router.register("auth/register", RegistrationViewSet, basename="register")

urlpatterns = router.urls
urlpatterns += [
    path("auth/login/", CustomLoginView.as_view(), name="login"),
]
