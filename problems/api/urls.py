from django.urls import path

from . import views

app_name = "problems"
urlpatterns = [
    path("", views.ProblemList.as_view(), name="list"),
    path("<int:pk>/", views.ProblemDetail.as_view(), name="detail"),
]
