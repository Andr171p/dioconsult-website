from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile


@receiver(post_save, sender=User)
def create_user_profile(sender: type[User], instance: User, created: bool, **kwargs) -> None:
    """Создание профиля пользователя при создании пользователя"""

    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profiles(sender: type[User], instance: User, **kwargs) -> None:
    """Сохранение профиля при сохранении пользоватлея"""

    instance.profile.save()
