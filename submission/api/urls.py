from django.urls import include, path
from . import views

app_name = 'api_submission'
urlpatterns = [
    path('<int:pk>', views.UserSubmissionDetail.as_view(), name='detail'),
    path('', views.UserSubmissionList.as_view(), name='list'),
    path(
        'daycount',
        views.UserSubmissionDayList.as_view(),
        name='list_daycount'),
    # path('<int:pk>/', views.UserSubmissionDetail.as_view(), name='detail'),
]
