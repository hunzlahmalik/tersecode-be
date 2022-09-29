from django.db import models
from django.utils.translation import gettext_lazy as _


class SubmissionAnalytics(models.Model):
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

    submission = models.OneToOneField(
        "Submission",
        on_delete=models.CASCADE,
        related_name="analytics",
        help_text="Submission",
    )
    status = models.CharField(
        max_length=1,
        choices=Status.choices,
        default=Status.PENDING,
        help_text="Submission status",
    )
    runtime = models.FloatField(help_text="Runtime in seconds", null=True, blank=True)
    memory = models.IntegerField(help_text="Memory in bytes", null=True, blank=True)
    result = models.JSONField(
        help_text="Result of the submission", null=True, blank=True
    )
