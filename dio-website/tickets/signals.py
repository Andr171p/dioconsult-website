from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from .models import Profile
from .models.invitation import Invitation


@receiver(post_save, sender=User)
def create_user_profile(sender: type[User], instance: User, created: bool, **kwargs) -> None:
    """Создание профиля пользователя при создании пользователя"""

    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profiles(sender: type[User], instance: User, **kwargs) -> None:
    """Сохранение профиля при сохранении пользоватлея"""

    instance.profile.save()


@receiver(post_save, sender=Invitation)
def send_invitation_email(
        sender: type[Invitation], instance: Invitation, created: bool, **kwargs
) -> None:
    """Отправка письма c ссылкой на регистрацию по email"""

    if created:
        link = f"{settings.SITE_URL}/invitation/{instance.token}/"
        html_message = render_to_string(
            "emails/invitation.html",
            {"link": link, "company": instance.company},
        )
        palin_message = strip_tags(html_message)
        send_mail(
            subject="Приглашение в тикет-систему",
            message=palin_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.email],
            html_message=html_message,
        )
