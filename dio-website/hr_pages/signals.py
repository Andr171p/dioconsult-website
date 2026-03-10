import os

from django.db.models.signals import post_delete
from django.dispatch import receiver

from .models import Vacancy



@receiver(post_delete, sender=Vacancy)
def delete_file(sender, instance, **kwargs):  # noqa: ARG001
    if hasattr(instance, "resume"):
        file_path = instance.resume.path
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception as e:  # noqa: BLE001
                raise Exception(f"Ошибка при удалении файла {file_path}: {e}") from None  # noqa: TRY002
