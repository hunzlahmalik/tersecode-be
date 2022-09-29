from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from problems.constants import PROBLEM_FILE_STORAGE_PATH, STATEMENT_EXTENSIONS
from .tag import Tag


class Problem(models.Model):
    class Difficulty(models.TextChoices):
        EASY = "E", _("Easy")
        MEDIUM = "M", _("Medium")
        HARD = "H", _("Hard")

    title = models.CharField(max_length=50)

    difficulty = models.CharField(
        max_length=1, choices=Difficulty.choices, default=Difficulty.EASY
    )
    statement = models.FileField(
        upload_to=PROBLEM_FILE_STORAGE_PATH,
        validators=[
            FileExtensionValidator(STATEMENT_EXTENSIONS),
        ],
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name="problems")
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.title
