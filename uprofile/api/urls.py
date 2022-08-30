from django.urls import path

from . import views

app_name = "uprofile"
urlpatterns = [
    # path("", views.ProfileList.as_view(), name="list"),
    path("<slug:username>/", views.ProfileDetail.as_view(), name="detail"),
]
