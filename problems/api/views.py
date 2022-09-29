from django.db.models import Count, Q
from rest_framework import generics, permissions

from submissions.models import Submission, SubmissionAnalytics
from .contants import FILTERS
from .serializers import (
    DiscussionSerializer,
    ProblemSerializer,
    TagSerializer,
    ProblemStats,
    UserProblemsStats,
)
from .. import models


class ProblemList(generics.ListAPIView):
    queryset = models.Problem.objects.all()
    serializer_class = ProblemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = FILTERS
    filterset_fields = ["title", "slug", "difficulty", "tags"]
    search_fields = ["title", "statement", "slug"]


class ProblemDetail(generics.RetrieveAPIView):
    queryset = models.Problem.objects.all()
    serializer_class = ProblemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class TagList(generics.ListCreateAPIView):
    queryset = models.Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class TagDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class DiscussionCreate(generics.CreateAPIView):
    queryset = models.Discussion.objects.all()
    serializer_class = DiscussionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
            problem=models.Problem.objects.get(id=self.kwargs["pk"]),
        )


class ProblemStatsView(generics.ListAPIView):
    serializer_class = ProblemStats
    permission_classes = [permissions.AllowAny]
    pagination_class = None

    def get_queryset(self):
        return (
            Submission.objects.filter(problem_id=self.kwargs["pk"])
            .values("user")
            .annotate(
                accepted=Count(
                    "id",
                    filter=Q(analytics__status=SubmissionAnalytics.Status.ACCEPTED),
                ),
                total=Count("id"),
            )
        )


class UserProblemsStatsView(generics.ListAPIView):
    serializer_class = UserProblemsStats
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        return (
            Submission.objects.filter(user=self.request.user)
            .values("problem")
            .annotate(
                accepted=Count(
                    "id",
                    filter=Q(analytics__status=SubmissionAnalytics.Status.ACCEPTED),
                ),
                total=Count("id"),
            )
        )
