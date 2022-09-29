from django.urls import path

from . import views

app_name = "submissions"
urlpatterns = [
    path("<int:pk>/", views.UserSubmissionDetail.as_view(), name="detail"),
    path(
        "problem/<int:pk>/stats/",
        views.ProblemSubmissionStatus.as_view(),
        name="detail",
    ),
    path("", views.UserSubmissionList.as_view(), name="list"),
    path("userstats/", views.UserSubmissionsStats.as_view(), name="list"),
    path("daycount/", views.UserSubmissionDayList.as_view(), name="list_daycount"),
    path(
        "monthcount/all/",
        views.UserSubmissionMonthList.as_view(),
        name="list_monthcount_all",
    ),
    path("monthcount/", views.MonthList.as_view(), name="list_monthcount"),
    # path('<int:pk>/', views.UserSubmissionDetail.as_view(), name='detail'),
]
