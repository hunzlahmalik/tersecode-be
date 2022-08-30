from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from problems.models import Problem, Language
from users.models import User
from .constants import CODE_EXTENSIONS, code_storage_path


class Submission(models.Model):
    """
    User Submission model.
    """
    class Status(models.TextChoices):
        """Submission status"""

        PENDING = "P", _("Pending")
        RUNNING = "B", _("Running")
        ACCEPTED = "A", _("Accepted")
        WRONG_ANSWER = "W", _("Wrong Answer")
        TIME_LIMIT_EXCEEDED = "T", _("Time Limit Exceeded")
        MEMORY_LIMIT_EXCEEDED = "M", _("Memory Limit Exceeded")
        OUTPUT_LIMIT_EXCEEDED = "O", _("Output Limit Exceeded")
        RUNTIME_ERROR = "R", _("Runtime Error")
        COMPILATION_ERROR = "C", _("Compilation Error")

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="submissions", help_text="User")
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name="submissions", help_text="Problem")
    language = models.ForeignKey(Language, on_delete=models.DO_NOTHING, related_name="submissions", help_text="Language")
    status = models.CharField(
        max_length=1, choices=Status.choices, default=Status.PENDING, help_text="Submission status"
    )
    code = models.FileField(
        upload_to=code_storage_path,
        validators=[FileExtensionValidator(CODE_EXTENSIONS)],
        help_text="Submission code"
    )
    timestamp = models.DateTimeField(auto_now_add=True, help_text="Submission timestamp")

    def __str__(self):
        return (
            self.user.username + " - " + self.problem.title + " - " + self.language.name
        )


class SubmissionAnalytics(models.Model):
    submission = models.OneToOneField(
        Submission, on_delete=models.CASCADE, related_name="analytics", help_text="Submission"
    )
    runtime = models.IntegerField( help_text="Runtime in seconds")
    memory = models.IntegerField( help_text="Memory in bytes")
