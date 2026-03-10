import os

from django.db.models.signals import post_delete
from django.dispatch import receiver

from .models import UploadDocument


@receiver(post_delete, sender=UploadDocument)
def delete_file(sender, instance, **kwargs):  # noqa: ARG001
    if hasattr(instance, "file"):
        file_path = instance.file.path
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception as e:  # noqa: BLE001
                raise Exception(f"Ошибка при удалении файла {file_path}: {e}") from None  # noqa: TRY002
