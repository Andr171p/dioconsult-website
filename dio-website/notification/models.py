from typing import ClassVar

from django.db import models
from django.utils import timezone
from modelcluster.models import ClusterableModel

from .email import send_admin_notification


class AdminNotification(ClusterableModel):
    title = models.CharField(max_length=255, verbose_name="Наименование")
    message = models.TextField(verbose_name="Сообщение")
    url = models.URLField(blank=True, null=True, verbose_name="Ссылка")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Дата создания")
    is_read = models.BooleanField(default=False, verbose_name="Просмотрено")

    class Meta:
        verbose_name = "Уведомление"
        verbose_name_plural = "Уведомления"
        ordering: ClassVar[list] = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.message}"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)

        # Отправляем email только при создании новой записи
        if is_new:
            send_admin_notification(self)
