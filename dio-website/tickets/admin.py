from typing import Any

from django.conf import settings
from django.contrib import admin, messages
from django.core.mail import send_mail
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from .models import Company, Invitation, Profile


class InvitationInline(admin.TabularInline):
    model = Invitation
    extra = 0
    fields = ("email", "created_at", "expires_at", "is_used", "token")
    readonly_fields = ("created_at", "expires_at", "is_used", "token")
    can_delete = False

    def has_add_permission(self, request: HttpRequest, obj: Company | None = None) -> bool:
        """Разрешает добавлять приглашение только если компания уже сохранена"""

        return obj is not None

    def has_change_permission(
            self, request: HttpRequest, obj: Invitation | None = None
    ) -> bool:
        """Запрет на изменение существующих приглашений (только просмотр)"""

        return False


class CompanyAdmin(admin.ModelAdmin):
    inlines = [InvitationInline]
    list_display = ("name", "inn", "phone")
    search_fields = ("name", "inn")

    def save_formset(
            self, request: HttpRequest, form: Any, formset: Any, change: Any
    ):
        """Перехват сохранённых инлайнов, чтобы отправить письмо для новых приглашений.
        При сохранении приглашения происходит автоматическая отправка на почту.
        """

        instances = formset.save(commit=False)
        for deleted_object in formset.deleted_objects:
            deleted_object.delete()
        for instance in instances:
            if instance.pk is None:
                instance.created_by = request.user
                instance.save()
        formset.save_m2m()


admin.site.register(Company, CompanyAdmin)
