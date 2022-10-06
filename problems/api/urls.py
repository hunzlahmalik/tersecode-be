from django.urls import path

from . import views

app_name = "problems"
urlpatterns = [
    path("", views.ProblemList.as_view(), name="list"),
    path("languages/", views.LanguagesList.as_view(), name="list"),
    path("<int:pk>/discussion/", views.DiscussionCreate.as_view(), name="discussion"),
    path("<int:pk>/", views.ProblemDetail.as_view(), name="detail"),
    path("<int:pk>/stats/", views.ProblemStatsView.as_view(), name="stats"),
    path("userstats/", views.UserProblemsStatsView.as_view(), name="stats"),
]
