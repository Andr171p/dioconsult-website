from django.conf import settings
from django.db import models


class Company(models.Model):
    """Модель представления компании клиента"""

    name = models.CharField(verbose_name="Название компании", max_length=255, unique=True)
    legal_name = models.CharField(verbose_name="Юридическое название", max_length=255, blank=True)
    inn = models.CharField(verbose_name="ИНН", max_length=12, blank=True, unique=True, null=True)
    phone = models.CharField(verbose_name="Телефон", max_length=20, blank=True)
    address = models.TextField(verbose_name="Адрес", blank=True)
    created_at = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Дата обновления", auto_now=True)

    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="companies",
        verbose_name="Пользователи",
        blank=True,
    )

    class Meta:
        verbose_name = "Компания"
        verbose_name_plural = "Компании"
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["inn"]),
        ]

    def __str__(self) -> str:
        return self.name
