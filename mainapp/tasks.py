from typing import Optional

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from authapp.models import CustomUser


@shared_task
def send_feedback_to_email(message_body: str, message_from: int = None) -> None:
    if message_from is not None:
        user_from = CustomUser.objects.filter(pk=message_from).first().get_full_name()
    else:
        user_from = 'Аноним'

    send_mail(
        subject=f'Feedback_from: {user_from}',
        message=message_body,
        recipient_list=['support@blms.local'],
        from_email='support@blms.local',
        fail_silently=False
    )
