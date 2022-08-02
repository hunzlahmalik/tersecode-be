from django.db import models
from django.core.validators import FileExtensionValidator
from problem.constants import PROBLEM_STORAGE_PATH


class Problem(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=50)
    difficulty = models.CharField(
        max_length=1,
        choices=[('E', 'Easy'),
                 ('M', 'Medium'),
                 ('H', 'Hard')],
        default='E'
    )
    statement = models.FileField(upload_to=PROBLEM_STORAGE_PATH,
                                 validators=[FileExtensionValidator(
                                     ['py', 'md', 'txt']), ]
                                 )
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
