from django.db import models


class Tag(models.Model):
    """
    Tag model.
    """

    name = models.CharField(max_length=50, unique=True, help_text="Tag name")

    def __str__(self):
        return self.name
