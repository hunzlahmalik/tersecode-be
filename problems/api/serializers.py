from rest_framework import serializers

from submissions.models import Submission
from ..models import Tag, Problem, Discussion, Language, TestCase, Solution


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields: list | None = kwargs.pop("fields", None)

        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class TagSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class SolutionSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Solution
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")
        extra_kwargs = {
            "problems": {"required": True},
            "solution": {"required": True},
        }


class LanguageSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Language
        fields = "__all__"
        read_only_fields = ["id"]


class TestCaseSerializer(DynamicFieldsModelSerializer):
    language = LanguageSerializer()

    class Meta:
        model = TestCase
        fields = "__all__"
        extra_kwargs = {
            "problems": {"required": True},
            "language": {"required": True},
            "input": {"required": True},
            "output": {"required": True},
            "hidden": {"required": True},
            "runtime": {"required": True},
            "memory": {"required": True},
        }


class DiscussionSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Discussion
        fields = "__all__"
        read_only_fields = ["id"]
        extra_kwargs = {
            "users": {"required": True},
            "problems": {"required": True},
            "content": {"required": True},
        }


class ProblemSerializer(serializers.ModelSerializer):
    solution = SolutionSerializer(read_only=True)
    tags = serializers.SerializerMethodField()
    testcases = serializers.SerializerMethodField()
    discussion = serializers.SerializerMethodField(required=False)
    is_solved = serializers.SerializerMethodField(required=False, read_only=True)

    class Meta:
        model = Problem
        fields = "__all__"
        read_only_fields = ["id", "slug"]
        extra_kwargs = {
            "title": {"required": True},
            "statement": {"required": True},
            "slug": {"required": True},
        }

    def get_testcases(self, obj: Problem):
        data = TestCaseSerializer(
            obj.testcases.filter(hidden=False),
            many=True,
            fields=["id", "input", "hidden", "output", "runtime", "memory", "language"],
        ).data

        return data

    def get_tags(self, obj: Problem):
        return [tag.name for tag in obj.tags.all()]

    def get_is_solved(self, obj: Problem):
        if self.context["request"] and self.context["request"].user.is_authenticated:
            return Submission.objects.filter(
                user=self.context["request"].user,
                problem=obj,
                status=Submission.Status.ACCEPTED,
            ).exists()
        return False

    def get_discussion(self, obj: Problem):
        data = DiscussionSerializer(
            obj.discussion_set.all(), many=True, fields=["id", "users", "content"]
        ).data

        return data

    def get_queryset(self):
        return Problem.objects.all()
