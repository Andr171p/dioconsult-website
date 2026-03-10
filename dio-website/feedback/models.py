from typing import ClassVar

from config.settings.dev import SITE_DOMAIN
from django.db import models
from notification.utils import create_admin_notification
from utils import get_tumen_time


class FeedbackMessage(models.Model):
    email = models.EmailField(verbose_name="Email")
    message = models.TextField(verbose_name="Сообщение")
    created_at = models.DateTimeField(default=get_tumen_time, verbose_name="Дата создания")
    is_processed = models.BooleanField(default=False, verbose_name="Просмотрено")

    class Meta:
        verbose_name = "Сообщение обратной связи"
        verbose_name_plural = "Сообщения обратной связи"
        ordering: ClassVar[list] = ["-created_at"]

    def __str__(self):
        return f"{self.email}"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new:
            create_admin_notification(
                title="Новое сообщение обратной связи",
                message=f"Сообщение обратной связи от {self.email}",
                url=f"{SITE_DOMAIN}/admin/snippets/feedback/feedbackmessage/edit/{self.id}/",  # type: ignore  # noqa: PGH003
            )
