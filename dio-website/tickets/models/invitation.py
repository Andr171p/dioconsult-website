from datetime import timedelta
from uuid import uuid4

from django.conf import settings
from django.db import models
from django.utils import timezone

from .profile import COUNTERPARTY_ROLES

EXPIRES_AT_DELTA_DAYS = 7


class Invitation(models.Model):
    """Приглашение на регистрацию пользователя (заказчика)"""

    email = models.EmailField(verbose_name="Email заказчика")
    counterparty = models.ForeignKey(
        "Counterparty",
        on_delete=models.CASCADE,
        related_query_name="invitations",
        null=True,
        blank=True,
    )
    token = models.UUIDField(default=uuid4, unique=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=timezone.now() + timedelta(days=EXPIRES_AT_DELTA_DAYS))
    is_used = models.BooleanField(default=False)

    default_counterparty_role = models.CharField(
        max_length=10, choices=COUNTERPARTY_ROLES, default="user"
    )

    def __str__(self) -> str:
        return f"Приглашение для {self.email} ({self.counterparty.name})"

    def is_valid(self) -> bool:
        """Активно ли ещё приглашение"""

        return not self.is_used and self.expires_at > timezone.now()

    def mark_as_used(self) -> None:
        """Пометить как использованное"""

        self.is_used = True
