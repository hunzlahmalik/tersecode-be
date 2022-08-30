from django.db import models

from problems.models import Problem, Language


class TestCase(models.Model):
    """
    TestCase model.
    """
    problem = models.ForeignKey(
        Problem, on_delete=models.CASCADE, related_name="testcases", help_text="Problem"
    )
    language = models.ForeignKey(
        Language, on_delete=models.CASCADE, related_name="testcases", help_text="Language"
    )

    input = models.JSONField(default=list)
    output = models.JSONField(default=list)
    hidden = models.BooleanField(default=True)

    runtime = models.IntegerField(default=1000, help_text="Time in seconds")  # limit
    memory = models.IntegerField(default=65536, help_text="Memory in bytes")  # limit

    def __str__(self):
        return self.problem.title + " - " + self.language.name + " - " + str(self.id)
