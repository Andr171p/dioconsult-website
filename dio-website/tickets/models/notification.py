# Модель уведомления, которое пользователь получает при изменении состояния системы

from django.conf import settings
from django.db import models


class Notification(models.Model):
    """Уведомление"""

    NOTIFICATION_TYPE_CHOICES = [
        ("status_change", "Изменение статуса"),
        ("new_message", "Новое сообщение"),
        ("new_ticket", "Новый тикет"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ticket = models.ForeignKey("Ticket", null=True, on_delete=models.SET_NULL)
    message = models.CharField(max_length=255)
    notification_type = models.CharField(choices=NOTIFICATION_TYPE_CHOICES, max_length=20)
    is_read = models.BooleanField(default=False)
    sent_email = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.notification_type}"
