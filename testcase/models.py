from email.policy import default
from django.db import models
from problem.models import Problem, Language


class TestCase(models.Model):
    """_summary_

    every test case can have multiple problem
    every problem can have multiple cases
    each case can belong to only one problems.
    every case can have multiple languages

    Args:
        models (_type_): _description_

    Returns:
        _type_: _description_
    """

    id = models.BigAutoField(primary_key=True)

    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    lanaguge = models.ForeignKey(Language, on_delete=models.CASCADE)

    input = models.JSONField(default=list)
    output = models.JSONField(default=list)
    hidden = models.BooleanField(default=True)

    time_limit = models.IntegerField(default=1000)
    memory_limit = models.IntegerField(default=65536)

    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.problem.title + ' - ' + self.lanaguge.name + ' - ' + str(self.id)
