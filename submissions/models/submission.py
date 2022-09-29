from django.core.validators import FileExtensionValidator
from django.db import models

from problems.models import Problem, Language
from users.models import User
from ..constants import CODE_EXTENSIONS, code_storage_path


class Submission(models.Model):
    """
    User Submission model.
    """

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="submissions", help_text="User"
    )
    problem = models.ForeignKey(
        Problem,
        on_delete=models.CASCADE,
        related_name="submissions",
        help_text="Problem",
    )
    language = models.ForeignKey(
        Language,
        on_delete=models.DO_NOTHING,
        related_name="submissions",
        help_text="Language",
    )
    code = models.FileField(
        upload_to=code_storage_path,
        validators=[FileExtensionValidator(CODE_EXTENSIONS)],
        help_text="Submission code",
    )
    timestamp = models.DateTimeField(
        auto_now_add=True, help_text="Submission timestamp"
    )

    def __str__(self):
        return (
            self.user.username + " - " + self.problem.title + " - " + self.language.name
        )
