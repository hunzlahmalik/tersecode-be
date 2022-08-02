from django.db import models
from django.contrib.auth.models import User
from problem.models import Problem, Language


class Submission(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.DO_NOTHING)
    code = models.TextField()
    status = models.CharField(max_length=1,
                              choices=[('P', 'Pending'),
                                       ('C', 'Compiling'),
                                       ('E', 'Error'),
                                       ('W', 'Waiting'),
                                       ('R', 'Running'),
                                       ('T', 'Time Limit Exceeded'),
                                       ('M', 'Memory Limit Exceeded'),
                                       ('I', 'Incorrect Answer'),
                                       ('S', 'Success')],
                              default='P')
    runtime = models.IntegerField(default=-1)
    memory = models.IntegerField(default=-1)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username + ' - ' + self.problem.title + ' - ' + self.language.name
