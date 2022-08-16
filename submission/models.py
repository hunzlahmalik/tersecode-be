from django.db import models
from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext_lazy as _

from account.models import User
from problem.models import Problem, Language
from .constants import CODE_EXTENSIONS, CODE_STORAGE_PATH


class Status(models.TextChoices):
    """ Submission status """
    PENDING = 'P', _('Pending')
    ACCEPTED = 'A', _('Accepted')
    WRONG_ANSWER = 'W', _('Wrong Answer')
    TIME_LIMIT_EXCEEDED = 'T', _('Time Limit Exceeded')
    MEMORY_LIMIT_EXCEEDED = 'M', _('Memory Limit Exceeded')
    OUTPUT_LIMIT_EXCEEDED = 'O', _('Output Limit Exceeded')
    RUNTIME_ERROR = 'R', _('Runtime Error')
    COMPILATION_ERROR = 'C', _('Compilation Error')


class Submission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=1,
                              choices=Status.choices,
                              default=Status.PENDING)
    code = models.FileField(
        upload_to=CODE_STORAGE_PATH, validators=[
            FileExtensionValidator(CODE_EXTENSIONS)])
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + ' - ' + \
            self.problem.title + ' - ' + self.language.name


class SubmissionAnalytics(models.Model):
    submission = models.OneToOneField(
        Submission, on_delete=models.CASCADE, related_name='analytics')
    runtime = models.IntegerField()
    memory = models.IntegerField()
