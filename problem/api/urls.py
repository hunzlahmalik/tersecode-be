from django.urls import include, path
from . import views

app_name = 'api_problem'
urlpatterns = [
    path('', views.ProblemList.as_view(), name='list'),
    path('<int:pk>/', views.ProblemDetail.as_view(), name='detail'),
]
