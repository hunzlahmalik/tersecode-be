from rest_framework import generics, permissions
from ..models import User
from .serializers import UserSerializer
from .permissions import IsCurrentUserOrReadOnly


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly]


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    lookup_url_kwarg = 'username'
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsCurrentUserOrReadOnly]
