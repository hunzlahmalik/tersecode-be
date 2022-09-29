from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import render
from django.urls import include
from django.urls import path
from rest_framework.documentation import include_docs_urls
from rest_framework.schemas import get_schema_view


def home(request):
    return render(request, "base.html")


urlpatterns = [
    path("", home, name="home"),
    path("admin/", admin.site.urls),
    path("problems/", include("problems.urls")),
    path("uprofile/", include("uprofile.urls")),
    path("users/", include("users.urls")),
    path("submissions/", include("submissions.urls")),
    path("api/v1/", include("api.v1.urls")),
    path("api-auth/", include("rest_framework.urls")),
    path("api/v1/docs/", include_docs_urls(title="TerseCode API"), name="api-docs"),
    path("api/v1/schema/", get_schema_view(title="TerseCode API"), name="api-schema"),
    path("__debug__/", include("debug_toolbar.urls")),
]

# only in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
