from rest_framework import serializers
from .. import models


class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Submission
        fields = '__all__'
        read_only_fields = ('id', 'timestamp')
        extra_kwargs = {
            'problem': {'required': True},
            'solution': {'required': True},
        }


class DayCountSerializer(serializers.Serializer):
    day = serializers.DateTimeField(format='%Y-%m-%d')
    count = serializers.IntegerField()
