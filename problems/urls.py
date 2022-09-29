from django.urls import path

from . import views

app_name = "problems"
urlpatterns = [
    path("", views.ProblemListView.as_view(), name="list"),
    path("<int:pk>/", views.ProblemDetailView.as_view(), name="detail"),
    path("<int:pk>/solution/", views.SolutionView.as_view(), name="solution"),
    path("<int:problem_id>/submit/", views.SubmissionView.as_view(), name="submit"),
]
