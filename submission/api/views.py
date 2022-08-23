from rest_framework import generics, permissions
from django.db import models
from django.db.models.functions import TruncDay
from ..models import Submission
from .serializers import SubmissionSerializer, DayCountSerializer


from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend


class UserSubmissionList(generics.ListCreateAPIView):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = [
        'problem',
        'user',
        'language',
        'status',
        'timestamp',
        'analytics__runtime']
    filterset_fields = {
        'problem': ['exact'],
        'user': ['exact'],
        'language': ['exact'],
        'status': ['exact'],
        'timestamp': ['gte', 'lte', 'exact', 'gt', 'lt'],
        'analytics__runtime': ['exact']
    }
    search_fields = ['problem__title',
                     'user__username', 'language__name', 'status']

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class UserSubmissionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset().filter(user=self.request.user)


class UserSubmissionDayList(generics.ListAPIView):
    """Give a list of submission count against days
    """
    serializer_class = DayCountSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    def get_queryset(self):
        return Submission.objects.filter(
            user=self.request.user).annotate(
            day=TruncDay('timestamp')).values('day').annotate(
            count=models.Count('id'))
