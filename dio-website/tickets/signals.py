from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from .models import Invitation


@receiver(post_save, sender=Invitation)
def send_invitation_email(
        sender: type[Invitation], instance: Invitation, created: bool, **kwargs
) -> None:
    """Отправка письма c ссылкой на регистрацию по email"""

    if created:
        link = f"{settings.SITE_URL}/invitation/activate/{instance.token}/"
        html_message = render_to_string(
            "emails/invitation.html",
            {"link": link, "counterparty": instance.counterparty},
        )
        plain_message = strip_tags(html_message)
        send_mail(
            subject="Приглашение в тикет-систему",
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.email],
            html_message=html_message,
        )
