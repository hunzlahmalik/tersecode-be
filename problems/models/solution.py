from django.core.validators import FileExtensionValidator
from django.db import models

from problems.constants import SOLUTION_EXTENSIONS, SOLUTION_STORAGE_PATH
from .problem import Problem


class Solution(models.Model):
    """
    Problem Solution model.
    """
    problem = models.OneToOneField(Problem, on_delete=models.CASCADE, related_name="solution", help_text="Problem")
    solution = models.FileField(
        upload_to=SOLUTION_STORAGE_PATH,
        validators=[
            FileExtensionValidator(SOLUTION_EXTENSIONS),
        ],
        help_text="Solution"
    )
    created_at = models.DateTimeField(auto_now_add=True, help_text="Solution timestamp")
    updated_at = models.DateTimeField(auto_now=True, help_text="Solution timestamp")

    def __str__(self):
        return self.problem.title
