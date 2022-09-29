from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)

from .token import MyTokenObtainPairView

app_name = "api"
urlpatterns = [
    path("token/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("users/", include("users.api.urls")),
    path("profile/", include("uprofile.api.urls")),
    path("problems/", include("problems.api.urls")),
    path("submissions/", include("submissions.api.urls")),
]
