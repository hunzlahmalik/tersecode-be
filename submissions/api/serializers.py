from rest_framework import serializers

from ..models import Submission, SubmissionAnalytics


class SubmissionAnalyticsSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source="get_status_display")

    class Meta:
        model = SubmissionAnalytics
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")
        extra_kwargs = {
            "submission": {"required": True},
        }


class SubmissionSerializer(serializers.ModelSerializer):
    analytics = SubmissionAnalyticsSerializer(read_only=True, required=False)

    class Meta:
        model = Submission
        fields = "__all__"
        read_only_fields = ("id", "timestamp")
        extra_kwargs = {
            "user": {"required": False},
            "problem": {"required": True, "allow_null": False},
            "code": {"required": True, "allow_null": False},
        }

    #
    def create(self, validated_data):
        if not self.context["request"].user.is_authenticated:
            raise serializers.ValidationError({"detail": ["User is not authenticated"]})
        if validated_data.get("user") is None:
            validated_data["user"] = self.context["request"].user
        else:
            if validated_data["user"] != self.context["request"].user:
                raise serializers.ValidationError(
                    {"detail": ["User is not authenticated"]}
                )
        data = super().create(validated_data)
        print("DATTS", data)
        return data


class DayCountSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    day = serializers.DateTimeField(format="%Y-%m-%d")
    count = serializers.IntegerField()
    accepted = serializers.IntegerField()


class MonthCountSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    month = serializers.DateTimeField(format="%Y-%m")
    count = serializers.IntegerField()
    accepted = serializers.IntegerField()


class ProblemSubmissionStatusSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    accepted = serializers.IntegerField()
    count = serializers.IntegerField()
    day = serializers.DateTimeField(format="%Y-%m-%d")


class UserSubmissionsStatsSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    accepted = serializers.IntegerField()
