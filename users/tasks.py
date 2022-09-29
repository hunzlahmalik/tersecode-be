from time import sleep

from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_email_task(email, subject, message, delay=5):
    sleep(delay)
    print("Sending email to: ", email)
    send_mail(
        subject=subject,
        message=message,
        recipient_list=[email],
        from_email=None,
    )
