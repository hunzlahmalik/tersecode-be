from rest_framework import generics
from api import permissions
from .serializer import ProfileSerializer
from ..models import Profile


class ProfileList(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [
        permissions.IsAuthenticated | permissions.IsAdminUser | permissions.IsSuperUser
    ]


class ProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = "user__username"
    lookup_url_kwarg = "username"
    permission_classes = [permissions.IsSuperUserORIsCurrentUserObject]
