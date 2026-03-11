from typing import Self

from django.db import models
from wagtail import blocks
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, PublishingPanel
from wagtail.contrib.settings.models import BaseGenericSetting, register_setting
from wagtail.fields import StreamField
from wagtail.models import DraftStateMixin, PreviewableMixin, RevisionMixin


@register_setting
class FooterSettings(
    DraftStateMixin, RevisionMixin, PreviewableMixin, BaseGenericSetting
):
    """Настройки футера сайта"""

    logo = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Логотип сайта",
        help_text="Логотип для footer. Рекомендуемый размер: 40x40px",
    )
    # Основные настройки
    copyright_text = models.CharField(
        max_length=200,
        default="© 2025 Все права защищены",
        verbose_name="Текст копирайта",
    )
    company_address = models.TextField(blank=True, verbose_name="Адрес компании")
    working_hours = models.CharField(
        max_length=100, blank=True, verbose_name="Часы работы"
    )

    # Социальные сети
    social_links = StreamField(
        [
            (
                "social",
                blocks.StructBlock(
                    [
                        (
                            "platform",
                            blocks.CharBlock(max_length=50, label="Платформа"),
                        ),
                        (
                            "href",
                            blocks.CharBlock(
                                max_length=200,
                                label="Ссылка (например, https://facebook.com или #contact)",
                            ),
                        ),
                        (
                            "icon",
                            blocks.CharBlock(
                                max_length=50,
                                label="Иконка (например, facebook, twitter)",
                            ),
                        ),
                    ],
                    label="Социальная сеть",
                ),
            )
        ],
        blank=True,
        use_json_field=True,
        verbose_name="Социальные сети",
    )

    # Секции ссылок
    company_section = StreamField(
        [
            (
                "item",
                blocks.StructBlock(
                    [
                        (
                            "title",
                            blocks.CharBlock(
                                max_length=100, label="Заголовок секции", required=False
                            ),
                        ),
                        (
                            "links",
                            blocks.ListBlock(
                                blocks.StructBlock(
                                    [
                                        (
                                            "text",
                                            blocks.CharBlock(
                                                max_length=100, label="Текст ссылки"
                                            ),
                                        ),
                                        (
                                            "href",
                                            blocks.CharBlock(
                                                max_length=200,
                                                label="Ссылка (например, /about или #contact)",
                                                blank=True,
                                            ),
                                        ),
                                    ]
                                )
                            ),
                        ),
                    ],
                    label="Секция компании",
                ),
            )
        ],
        blank=True,
        use_json_field=True,
        verbose_name="Секции компании",
    )

    solutions_section = StreamField(
        [
            (
                "item",
                blocks.StructBlock(
                    [
                        (
                            "title",
                            blocks.CharBlock(
                                max_length=100, label="Заголовок секции", required=False
                            ),
                        ),
                        (
                            "links",
                            blocks.ListBlock(
                                blocks.StructBlock(
                                    [
                                        (
                                            "text",
                                            blocks.CharBlock(
                                                max_length=100, label="Текст ссылки"
                                            ),
                                        ),
                                        (
                                            "href",
                                            blocks.CharBlock(
                                                max_length=200,
                                                label="Ссылка (например, /solutions или #solutions)",
                                                blank=True,
                                            ),
                                        ),
                                    ]
                                )
                            ),
                        ),
                    ],
                    label="Секция решений",
                ),
            )
        ],
        blank=True,
        use_json_field=True,
        verbose_name="Секции решений",
    )

    services_section = StreamField(
        [
            (
                "item",
                blocks.StructBlock(
                    [
                        (
                            "title",
                            blocks.CharBlock(
                                max_length=100, label="Заголовок секции", required=False
                            ),
                        ),
                        (
                            "links",
                            blocks.ListBlock(
                                blocks.StructBlock(
                                    [
                                        (
                                            "text",
                                            blocks.CharBlock(
                                                max_length=100, label="Текст ссылки"
                                            ),
                                        ),
                                        (
                                            "href",
                                            blocks.CharBlock(
                                                max_length=200,
                                                label="Ссылка (например, /services или #services)",
                                                blank=True,
                                            ),
                                        ),
                                    ]
                                )
                            ),
                        ),
                    ],
                    label="Секция услуг",
                ),
            )
        ],
        blank=True,
        use_json_field=True,
        verbose_name="Секции услуг",
    )

    # Кнопка "Связаться с нами"
    contact_button_text = models.CharField(
        max_length=50, default="Связаться с нами", verbose_name="Текст кнопки"
    )
    contact_button_href = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Ссылка кнопки (например, #contact или /contact)",
    )

    # Панели админки
    content_panels = [
        MultiFieldPanel(
            [
                FieldPanel("copyright_text"),
                FieldPanel("company_address"),
                FieldPanel("working_hours"),
                FieldPanel("social_links"),
                FieldPanel("company_section"),
                FieldPanel("solutions_section"),
                FieldPanel("services_section"),
                FieldPanel("contact_button_text"),
                FieldPanel("contact_button_href"),
            ],
            heading="Настройки футера",
        ),
    ]

    publish_panels = [PublishingPanel()]

    class Meta:
        verbose_name = "Футер"
        verbose_name_plural = "Футер"

    def get_preview_template(self, request, mode_name) -> str:
        return "base.html"

    def get_preview_context(self, request, mode_name) -> dict[str, Self]:
        return {"settings": self}
