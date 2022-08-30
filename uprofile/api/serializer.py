from rest_framework import serializers
from users.api.serializers import UserSerializer
from ..models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)

    class Meta:
        model = Profile
        fields = "__all__"

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", None)
        if user_data:
            try:
                user = UserSerializer.update(UserSerializer(), instance.user, user_data)
                instance.user = user
            except serializers.ValidationError as e:
                raise serializers.ValidationError({"user": e.detail})
        return super().update(instance, validated_data)
