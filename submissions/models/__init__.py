from django.db.models.signals import post_save
from django.dispatch import receiver

from .analytics import SubmissionAnalytics
from .submission import Submission
from ..tasks import task_after_submission


@receiver(post_save, sender=Submission)
def create_analytics(sender, instance, created, **kwargs):
    print("post_save", instance, created)
    if created:
        analytics_ = SubmissionAnalytics(submission=instance)
        analytics_.save()
        task_after_submission.delay(analytics_.id)
