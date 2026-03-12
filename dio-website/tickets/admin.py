from typing import Any

from django.contrib import admin, messages
from django.db import transaction
from django.http import HttpRequest

from .forms import InvitationInlineForm
from .models import Counterparty, Invitation


@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = ("email", "counterparty", "created_by", "created_at", "is_used", "expires_at")
    list_filter = ("is_used", "counterparty")
    search_fields = ("email", "counterparty__name")
    readonly_fields = ("token", "created_at", "expires_at", "created_by")


class InvitationInline(admin.TabularInline):
    model = Invitation
    form = InvitationInlineForm
    extra = 1
    max_num = 10
    fields = (
        "email",
        "default_counterparty_role",
        "created_at",
        "expires_at",
        "is_used",
        "token",
        "created_by",
    )
    readonly_fields = (
        "created_at",
        "expires_at",
        "is_used",
        "token",
        "created_by",
    )
    can_delete = False

    def has_add_permission(self, request: HttpRequest, obj: Counterparty | None = None) -> bool:
        """Разрешает добавлять приглашение только если компания уже сохранена"""

        return obj is not None

    def has_change_permission(
            self, request: HttpRequest, obj: Invitation | None = None
    ) -> bool:
        """Запрет на изменение существующих приглашений (только просмотр)"""

        return False


class CounterpartyAdmin(admin.ModelAdmin):
    inlines = [InvitationInline]
    list_display = ("name", "legal_name", "inn", "phone", "email", "users_count")
    search_fields = ("name", "legal_name", "inn")
    list_filter = ("is_active",)
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        (None, {"fields": ("name", "legal_name", "inn", "kpp")}),
        ("Контакты", {"fields": ("phone", "email", "address")}),
        ("Статус", {"fields": ("is_active", "created_at", "updated_at")}),
    )

    def users_count(self, obj):
        return obj.counterpartyuser_set.count()

    users_count.short_description = "Пользователей"

    def save_formset(
            self, request: HttpRequest, form: Any, formset: Any, change: Any
    ):
        """Перехват сохранённых инлайнов, чтобы отправить письмо для новых приглашений.
        При сохранении приглашения происходит автоматическая отправка на почту.
        """

        if formset.model != Invitation:
            return super().save_formset(request, form, formset, change)
        instances = formset.save(commit=False)
        with transaction.atomic():
            for deleted_object in formset.deleted_objects:
                deleted_object.delete()
            for instance in instances:
                if instance.pk is None:
                    instance.created_by = request.user
                    instance.save()
                else:
                    instance.save()
        formset.save_m2m()
        new_invitations = [
            instance for instance in instances if not instance.pk or instance._state.adding
        ]
        if new_invitations:
            messages.success(
                request, f"Создано и отпралено {len(new_invitations)} приглашений"
            )
        return None


admin.site.register(Counterparty, CounterpartyAdmin)
