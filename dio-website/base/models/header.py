from typing import Self

from django.db import models
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, PublishingPanel
from wagtail.blocks import (
    CharBlock,
    ChoiceBlock,
    ListBlock,
    PageChooserBlock,
    StructBlock,
    URLBlock,
)
from wagtail.contrib.settings.models import BaseGenericSetting, register_setting
from wagtail.fields import StreamField
from wagtail.models import DraftStateMixin, Page, PreviewableMixin, RevisionMixin


@register_setting
class HeaderSettings(
    DraftStateMixin, RevisionMixin, PreviewableMixin, BaseGenericSetting
):
    """Настройки хедера сайта"""

    class Meta:
        verbose_name = "Хидер"
        verbose_name_plural = "Хидер"

    # Основные поля
    logo = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Логотип сайта (рекомендуемый размер: 40x40px)",
    )
    site_title = models.CharField(
        max_length=255,
        blank=True,
        default="",
        help_text="Название сайта, отображаемое рядом с логотипом",
    )
    consultation_button_text = models.CharField(
        max_length=255,
        default="Оставить заявку",
        help_text="Текст кнопки консультации",
    )
    consultation_page = models.ForeignKey(
        Page,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Выберите страницу для ссылки на консультацию",
    )

    nav_items = StreamField(
        [
            (
                "nav_item",
                StructBlock(
                    [
                        (
                            "name",
                            CharBlock(
                                max_length=255,
                                required=True,
                                label="Название пункта*",
                                help_text="Название пункта меню",
                            ),
                        ),
                        (
                            "page",
                            PageChooserBlock(
                                required=False,
                                label="Страница",
                                help_text="Выберите страницу для ссылки",
                            ),
                        ),
                        (
                            "external_url",
                            URLBlock(
                                required=False,
                                label="Внешняя ссылка",
                                help_text="Укажите внешний URL, если страница не выбрана",
                            ),
                        ),
                        (
                            "menu_type",
                            ChoiceBlock(
                                choices=[
                                    ("none", "Без подменю"),
                                    ("simple", "Простое подменю"),
                                ],
                                default="none",
                                label="Тип меню*",
                                help_text="Выберите тип подменю",
                            ),
                        ),
                        (
                            "simple_dropdown_items",
                            ListBlock(
                                StructBlock(
                                    [
                                        (
                                            "name",
                                            CharBlock(
                                                max_length=255,
                                                required=True,
                                                label="Название подпункта*",
                                                help_text="Название подпункта",
                                            ),
                                        ),
                                        (
                                            "page",
                                            PageChooserBlock(
                                                required=False,
                                                label="Страница",
                                                help_text="Выберите страницу для ссылки",
                                            ),
                                        ),
                                        (
                                            "external_url",
                                            URLBlock(
                                                required=False,
                                                label="Внешняя ссылка",
                                                help_text="Укажите внешний URL, если страница не выбрана",
                                            ),
                                        ),
                                    ]
                                ),
                                required=False,
                                label="Простые элементы подменю",
                                help_text="Используется для типа 'Простое подменю'",
                            ),
                        ),
                    ],
                    icon="list-ul",
                    label="Пункт меню",
                ),
            )
        ],
        use_json_field=True,
        blank=True,
        null=True,
    )

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("logo"),
                FieldPanel("site_title"),
                FieldPanel("consultation_button_text"),
                FieldPanel("consultation_page"),
                FieldPanel("nav_items"),
            ],
            heading="Основные настройки хедера",
        ),
        PublishingPanel(),
    ]

    def get_preview_template(self, request, mode_name) -> str:
        return "base.html"

    def get_preview_context(self, request, mode_name) -> dict[str, Self]:
        return {"settings": self}
