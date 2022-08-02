from django.db import models
from .problem import Problem
from .tag import Tag


class ProblemTag(models.Model):
    id = models.BigAutoField(primary_key=True)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.problem.title + ' - ' + self.tag.name

    class Meta:
        unique_together = ('problem', 'tag')
