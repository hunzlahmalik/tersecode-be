from django.db import models
from django.db.models.functions import TruncDay, TruncMonth
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions
from rest_framework.filters import SearchFilter, OrderingFilter

from .serializers import (
    SubmissionSerializer,
    DayCountSerializer,
    MonthCountSerializer,
    ProblemSubmissionStatusSerializer,
    UserSubmissionsStatsSerializer,
)
from ..models import Submission, SubmissionAnalytics


class UserSubmissionList(generics.ListCreateAPIView):
    queryset = Submission.objects.prefetch_related("analytics").all()
    serializer_class = SubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = {
        "problem": ["exact"],
        "user": ["exact"],
        "language": ["exact"],
        "analytics__status": ["exact"],
        "timestamp": ["gte", "lte", "exact", "gt", "lt"],
        "analytics__runtime": ["exact"],
    }
    search_fields = ["problem__title", "user__username", "language__name", "status"]

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class UserSubmissionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset().filter(user=self.request.user)


class UserSubmissionDayList(generics.ListAPIView):
    """Give a list of submissions count against days"""

    serializer_class = DayCountSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = None

    def get_queryset(self):
        return (
            Submission.objects.filter(user=self.request.user)
            .annotate(day=TruncDay("timestamp"))
            .values("day")
            .annotate(count=models.Count("id"))
            .annotate(
                accepted=models.Count(
                    "id",
                    filter=models.Q(
                        analytics__status=SubmissionAnalytics.Status.ACCEPTED
                    ),
                )
            )
        )


class UserSubmissionMonthList(generics.ListAPIView):
    """Give a list of submissions count against days"""

    serializer_class = MonthCountSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = None

    def get_queryset(self):
        return (
            Submission.objects.filter(user=self.request.user)
            .annotate(month=TruncMonth("timestamp"))
            .values("month")
            .annotate(count=models.Count("id"))
            .annotate(
                accepted=models.Count(
                    "id",
                    filter=models.Q(
                        analytics__status=SubmissionAnalytics.Status.ACCEPTED
                    ),
                )
            )
        )


class MonthList(generics.ListAPIView):
    """Give a list of submissions count against days"""

    serializer_class = MonthCountSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = None

    def get_queryset(self):
        return (
            Submission.objects.all()
            .annotate(month=TruncMonth("timestamp"))
            .values("month")
            .annotate(count=models.Count("id"))
            .annotate(
                accepted=models.Count(
                    "id",
                    filter=models.Q(
                        analytics__status=SubmissionAnalytics.Status.ACCEPTED
                    ),
                )
            )
        )


class ProblemSubmissionStatus(generics.ListAPIView):
    """Give a list of submissions count against days"""

    serializer_class = ProblemSubmissionStatusSerializer
    pagination_class = None

    def get_queryset(self):
        return (
            Submission.objects.filter(problem=self.kwargs["pk"])
            .annotate(day=TruncDay("timestamp"))
            .values("day")
            .annotate(count=models.Count("id"))
            .annotate(
                accepted=models.Count(
                    "id",
                    filter=models.Q(
                        analytics__status=SubmissionAnalytics.Status.ACCEPTED
                    ),
                )
            )
            .order_by("-day")
        )


class UserSubmissionsStats(generics.ListAPIView):
    serializer_class = UserSubmissionsStatsSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        return (
            Submission.objects.filter(user=self.request.user)
            .values("user")
            .annotate(
                count=models.Count("id"),
                accepted=models.Count(
                    "id",
                    filter=models.Q(
                        analytics__status=SubmissionAnalytics.Status.ACCEPTED
                    ),
                ),
            )
        )
