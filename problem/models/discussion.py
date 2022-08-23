from django.db import models
from account.models import User
from .problem import Problem


class Discussion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + ' - ' + \
            self.problem.title + ' - ' + self.content[:10]
