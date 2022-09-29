from django.urls import path

from . import views

app_name = "uprofile"
urlpatterns = [
    path("", views.UserDetailView.as_view(), name="detail"),
    path("update", views.UserUpdateView.as_view(), name="update"),
]
