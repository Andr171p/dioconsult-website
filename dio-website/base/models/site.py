from typing import Self

from django.db import models
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, PublishingPanel
from wagtail.contrib.settings.models import BaseGenericSetting, register_setting
from wagtail.contrib.settings.models import BaseSiteSetting as SiteSetting


@register_setting
class SiteSettings(BaseGenericSetting):
    """Настройки сайта"""

    name = models.CharField(
        max_length=100,
        verbose_name="Название компании",
        default="Название компании",
        blank=True,
    )
    icon = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Логотип компании",
    )
    address = models.TextField(
        max_length=100,
        verbose_name="г.Тюмень",
        blank=True,
    )

    content_panels = [
        MultiFieldPanel(
            [
                FieldPanel("name"),
                FieldPanel("icon"),
                FieldPanel("address"),
            ],
            heading="Основные настройки",
        ),
    ]

    publish_panels = [PublishingPanel()]

    class Meta:
        verbose_name = "Инофрмация о сайте"

    def get_preview_template(self, request, mode_name) -> str:  # noqa: ANN001
        return "base.html"

    def get_preview_context(self, request, mode_name) -> dict[str, Self]:  # noqa: ANN001
        return {"settings": self}


@register_setting
class ThemeSettings(SiteSetting):
    THEME_CHOICES = (
        ("none", "Нет темы"),
        ("new_year", "Новый год (снежинки)"),
        ("autumn", "Осень (листья)"),
        # Добавьте больше, если нужно: ('spring', 'Весна (цветы)'), etc.
    )

    theme = models.CharField(
        max_length=20,
        choices=THEME_CHOICES,
        default="none",
        help_text="Выберите сезонную тему для сайта",
    )

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("theme"),
            ],
            heading="Сезонные темы",
        ),
    ]

    class Meta:
        verbose_name = "Темы"
