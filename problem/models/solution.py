from django.db import models
from django.core.validators import FileExtensionValidator
from problem.constants import SOLUTION_STORAGE_PATH
from .problem import Problem
from .language import Language


class Solution (models.Model):
    id = models.BigAutoField(primary_key=True)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    solution = models.FileField(upload_to=SOLUTION_STORAGE_PATH,
                                validators=[FileExtensionValidator(
                                    ['py', 'md', 'txt']), ]
                                )

    def __str__(self):
        return self.problem.title + ' - ' + self.language.name

    class Meta:
        unique_together = ('problem', 'language')
