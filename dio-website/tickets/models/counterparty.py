# Реализация модели контрагента

from django.conf import settings
from django.db import models


class Counterparty(models.Model):
    """Справочник контрагентов (кдиентов)"""

    name = models.CharField(verbose_name="Название", max_length=255, unique=True)
    legal_name = models.CharField(
        verbose_name="Юридическое наименование", max_length=255, blank=True
    )
    inn = models.CharField(verbose_name="ИНН", max_length=12, blank=True, unique=True, null=True)
    kpp = models.CharField(verbose_name="КПП", max_length=9, blank=True)
    phone = models.CharField(verbose_name="Телефон", max_length=20, blank=True)
    email = models.EmailField(verbose_name="Основной email", blank=True)
    address = models.TextField(verbose_name="Адрес", blank=True)
    is_active = models.BooleanField(verbose_name="Активен", default=True)

    created_at = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Дата обновления", auto_now=True)

    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="counterparties",
        verbose_name="Пользователи контрагента",
        blank=True,
    )

    class Meta:
        verbose_name = "Контрагент"
        verbose_name_plural = "Контрагенты"
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=["inn"], condition=models.Q(inn__isnull=False), name="unique_inn"
            )
        ]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["inn"]),
        ]

    def __str__(self) -> str:
        return self.name
