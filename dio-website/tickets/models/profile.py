# Роли и права доступа пользователей системы

from django.conf import settings
from django.db import models

COUNTERPARTY_ROLES = (("admin", "Администратор"), ("user", "Пользователь"))


class Profile(models.Model):
    """Профиль -расширение стандартной модели пользователя"""

    USER_ROLES = (
        ("counterparty_admin", "Админ контрагента"),
        ("counterparty_user", "Сотрудник контрагента"),
        ("support_agent", "Агент поддержки"),
        ("support_manager", "Менеджер поддержки"),
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name="Пользователь"
    )
    role = models.CharField(
        "Роль в системе",
        max_length=20,
        choices=USER_ROLES,
        default="company_user"
    )
    avatar = models.ImageField(
        verbose_name="Аватар",
        upload_to="avatars/",
        null=True,
        blank=True
    )
    email_notifications_enabled = models.BooleanField(
        verbose_name="Отправка email уведомлений", default=True
    )

    # Поля, специфичные для агентов поддержки
    department = models.CharField(verbose_name="Отдел", max_length=100, blank=True)
    max_assigned_tickets = models.PositiveSmallIntegerField(
        verbose_name="Макс. тикетов", default=10
    )

    created_at = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Дата обновления", auto_now=True)

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    def __str__(self) -> str:
        return f"{self.user.get_full_name()} ({self.get_role_display()})"


class CounterpartyUser(models.Model):
    """Роль пользователя внутри конкретного контрагента. Админ котрагента может просмативать
    все тикеты своей компании.
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    counterparty = models.ForeignKey("Counterparty", on_delete=models.CASCADE)
    role = models.CharField(
        choices=COUNTERPARTY_ROLES,
        max_length=10,
        default="user"
    )
    can_create_tickets = models.BooleanField(default=True)
    can_view_all_tickets = models.BooleanField(default=False)  # только для admin

    class Meta:
        unique_together = ("user", "counterparty")
        verbose_name = "Связь пользователь-контрагент"

    def __str__(self) -> str:
        return "Роль пользователя"
