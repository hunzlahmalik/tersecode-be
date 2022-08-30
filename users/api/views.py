from rest_framework import generics
from api import permissions
from .serializers import UserSerializer
from ..models import User


class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [
        permissions.IsAuthenticated | permissions.IsAdminUser | permissions.IsSuperUser
    ]


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "username"
    lookup_url_kwarg = "username"
    permission_classes = [permissions.IsSuperUserORIsCurrentUserObject]
