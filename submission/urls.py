from django.urls import path
from . import views

app_name = 'submission'
urlpatterns = [
    path(
        '',
        views.SubmissionIndexView.as_view(),
        name='list'),
    path(
        '<int:pk>/',
        views.SubmissionDetailView.as_view(),
        name='detail'),
    path(
        '<slug:slug>/',
        views.SubmissionListView.as_view(),
        name='submissions'),
]
