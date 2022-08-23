from rest_framework import serializers
from ..models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']
        read_only = (
            'id',
            'username',
            'email',
            'is_staff',
            'is_active',
            'is_superuser',
            'date_joined',
            'last_login',
            'user_permissions')
        extra_kwargs = {
            'username': {'required': True},
            'email': {'required': True},
            'id': {'read_only': True},
            'is_staff': {'read_only': True},
            'is_active': {'read_only': True},
            'is_superuser': {'read_only': True},
            'date_joined': {'read_only': True},
            'last_login': {'read_only': True},
            'user_permissions': {'read_only': True}
        }
