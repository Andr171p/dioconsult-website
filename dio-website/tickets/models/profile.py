from django.conf import settings
from django.db import models


class Profile(models.Model):
    """Профиль -расширение стандартной модели пользователя"""

    USER_ROLES = (
        ("company_admin", "Администратор компании"),
        ("company_user", "Сотрудник компании"),
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
        "Аватар",
        upload_to="avatars/",
        null=True,
        blank=True
    )

    # Поля, специфичные для агентов поддержки
    department = models.CharField("Отдел", max_length=100, blank=True)
    max_assigned_tickets = models.PositiveSmallIntegerField(
        verbose_name="Макс. тикетов", default=10
    )

    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField("Дата обновления", auto_now=True)

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    def __str__(self) -> str:
        return f"{self.user.get_full_name()} ({self.get_role_display()})"
