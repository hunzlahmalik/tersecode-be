from time import sleep

from celery import shared_task

from .models import Problem


@shared_task
def count_problems(request):
    sleep(20)
    return Problem.objects.count()
