from django.db import models
from django.core.validators import FileExtensionValidator
from problem.constants import SOLUTION_EXTENSIONS, SOLUTION_STORAGE_PATH
from .problem import Problem
from .language import Language


class Solution (models.Model):
    problem = models.OneToOneField(Problem, on_delete=models.CASCADE)
    solution = models.FileField(upload_to=SOLUTION_STORAGE_PATH,
                                validators=[FileExtensionValidator(
                                    SOLUTION_EXTENSIONS), ]
                                )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.problem.title
