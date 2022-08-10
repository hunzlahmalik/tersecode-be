from django.urls import path
from . import views

app_name = 'account'
urlpatterns = [
    # redircts to user own page if logged in, else login page
    path('', views.UserIndexView.as_view(), name='index'),

    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('signup/', views.CustomSignUpView.as_view(), name='signup'),

    path('<slug:slug>/', views.UserDetailView.as_view(), name='detail'),
    path('<slug:slug>/update', views.UserUpdateView.as_view(), name='update'),
]
