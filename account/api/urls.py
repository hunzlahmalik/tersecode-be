from django.urls import include, path
from . import views

app_name = 'api_user'
urlpatterns = [
    path('', views.UserList.as_view(), name='list'),
    path('<slug:username>/', views.UserDetail.as_view(), name='detail'),
]
