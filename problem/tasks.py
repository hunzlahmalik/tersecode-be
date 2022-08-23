from celery import shared_task
from .models import Problem


@shared_task
def count_problems():
    return Problem.objects.count()
