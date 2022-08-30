from django.urls import include, path
from rest_framework.documentation import include_docs_urls
from rest_framework.schemas import get_schema_view
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = "api"
urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("users/", include("users.api.urls")),
    path("profile/", include("uprofile.api.urls")),
    path("problems/", include("problems.api.urls")),
    path("submissions/", include("submissions.api.urls")),
]
