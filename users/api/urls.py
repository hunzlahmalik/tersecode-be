from django.urls import path

from . import views

app_name = "users"
urlpatterns = [
    path("", views.UserList.as_view(), name="list"),
    path("signup/", views.UserCreate.as_view(), name="signup"),
    path("<slug:username>/", views.UserDetail.as_view(), name="detail"),
]
