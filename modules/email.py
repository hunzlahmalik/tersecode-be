from django.core.mail import send_mail
from django.conf import settings


def send_email(
        subject,
        message,
        to_email,
        from_email=settings.EMAIL_HOST_USER):
    return send_mail(subject, message, from_email, [to_email])
