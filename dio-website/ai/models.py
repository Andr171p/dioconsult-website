from typing import ClassVar

from django.core.exceptions import ValidationError
from django.core.files.storage import default_storage
from django.db import models

from .rest import upload_document


class UploadDocument(models.Model):
    file = models.FileField(upload_to="upload/%Y/%m/%d/", verbose_name="Файл")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Загруженные документы"
        ordering: ClassVar[list] = ["-created_at"]

    def __str__(self) -> str:
        return f"Загруженный документ номер {self.id}"  # pyright: ignore[reportAttributeAccessIssue]

    def clean(self) -> None:
        """Проверка расширения файла перед сохранением."""
        if self.file:
            file_extension = self.file.name.split(".")[-1].lower()
            allowed_extensions = ["pdf", "docx", "doc", "txt", "md"]
            if file_extension not in allowed_extensions:
                raise ValidationError(
                    f"Недопустимое расширение файла. Допустимы только: {', '.join(allowed_extensions)}"  # noqa: E501
                )

    def save(self, *args, **kwargs) -> None:
        if not self.pk and not self.file:
            super().save(*args, **kwargs)
            return

        self.clean()
        result = upload_document(self.file)  # type: ignore  # noqa: PGH003
        if result:
            super().save(*args, **kwargs)
        else:
            self.file = None

    def delete(self, *args, **kwargs) -> None:
        # Удаляем файл перед удалением объекта
        if self.file:
            default_storage.delete(self.file.name)
        super().delete(*args, **kwargs)
