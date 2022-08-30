from rest_framework import generics, permissions

from .contants import FILTERS
from .serializers import ProblemSerializer, TagSerializer
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
