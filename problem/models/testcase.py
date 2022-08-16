from email.policy import default
from django.db import models
from problem.models import Problem, Language


class TestCase(models.Model):
    id = models.BigAutoField(primary_key=True)

    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    lanaguge = models.ForeignKey(Language, on_delete=models.CASCADE)

    input = models.JSONField(default=list)
    output = models.JSONField(default=list)
    hidden = models.BooleanField(default=True)

    runtime = models.IntegerField(default=1000)  # limit
    memory = models.IntegerField(default=65536)  # limit

    def __str__(self):
        return self.problem.title + ' - ' + \
            self.lanaguge.name + ' - ' + str(self.id)
