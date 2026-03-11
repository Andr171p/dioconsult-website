from typing import Self

from django import forms
from django.conf import settings
from django.db import models
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, PublishingPanel
from wagtail.blocks import CharBlock
from wagtail.contrib.settings.models import BaseGenericSetting, register_setting
from wagtail.fields import StreamField
from wagtail.models import DraftStateMixin, PreviewableMixin, RevisionMixin


class ContactSubmission(models.Model):
    """Отправка контакта"""

    name = models.CharField(max_length=255, verbose_name="Имя")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Телефон")
    message = models.TextField(verbose_name="Сообщение")
    submitted_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата отправки")

    panels = [
        FieldPanel("name"),
        FieldPanel("email"),
        FieldPanel("phone"),
        FieldPanel("message"),
        FieldPanel("submitted_at"),
    ]

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"

    def __str__(self) -> str:
        return f"Заявка от {self.name} ({self.email})"


@register_setting
class ContactSettings(
    DraftStateMixin, RevisionMixin, PreviewableMixin, BaseGenericSetting
):
    """Настройки контактов"""

    form_recipient_email = models.EmailField(
        blank=True,
        verbose_name="Email для заявок",
        help_text="Email, на который будут отправляться заявки из формы.",
    )

    notification_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='contact_notifications',
        verbose_name="Пользователи для уведомлений",
        help_text="Выберите пользователей, которые будут получать уведомления в админке.",
    )
    section_title = models.CharField(
        max_length=100, default="Связаться с нами", verbose_name="Заголовок секции"
    )
    section_description = models.TextField(
        default=(
            "Готовы обсудить автоматизацию вашего бизнеса?"
            "Свяжитесь с нашими экспертами для получения персональной консультации."
        ),
        verbose_name="Описание секции",
    )
    primary_phone = models.CharField(
        max_length=20, blank=True, verbose_name="Основной телефон"
    )
    secondary_phone = models.CharField(
        max_length=20, blank=True, verbose_name="Дополнительный телефон"
    )
    primary_email = models.EmailField(blank=True, verbose_name="Основной email")
    secondary_email = models.EmailField(blank=True, verbose_name="Дополнительный email")
    address = models.TextField(blank=True, verbose_name="Адрес")
    working_hours = models.TextField(
        default="Пн-Пт: 9:00 - 18:00, Сб-Вс: по договоренности",
        verbose_name="Режим работы",
    )
    map_placeholder_text = models.TextField(
        default="г. Москва, ул. Тверская, д. 15", verbose_name="Текст под картой"
    )
    # Услуги
    services = StreamField(
        [("service", CharBlock(max_length=100, label="Название услуги"))],
        blank=True,
        use_json_field=True,
        verbose_name="Список услуг",
    )
    # Форма
    form_title = models.CharField(
        max_length=100, default="Оставить заявку", verbose_name="Заголовок формы"
    )
    privacy_policy_text = models.TextField(
        default=(
            "Нажимая кнопку, вы соглашаетесь с <a href='/privacy-policy/'>"
            "политикой обработки персональных данных</a>"
        ),
        verbose_name="Текст политики конфиденциальности",
    )

    content_panels = [
        MultiFieldPanel(
            [
                FieldPanel("form_recipient_email"),
                FieldPanel("notification_users", widget=forms.CheckboxSelectMultiple),
                FieldPanel("section_title"),
                FieldPanel("section_description"),
                FieldPanel("primary_phone"),
                FieldPanel("secondary_phone"),
                FieldPanel("primary_email"),
                FieldPanel("secondary_email"),
                FieldPanel("address"),
                FieldPanel("working_hours"),
                FieldPanel("map_placeholder_text"),
                FieldPanel("services"),
                FieldPanel("form_title"),
                FieldPanel("privacy_policy_text"),
            ],
            heading="Настройки контактов",
        ),
    ]

    publish_panels = [PublishingPanel()]

    class Meta:
        verbose_name = "Контакты"
        verbose_name_plural = "Контакты"

    def get_preview_template(self, request, mode_name) -> str:  # noqa: ANN001
        return "base.html"

    def get_preview_context(self, request, mode_name) -> dict[str, Self]:  # noqa: ANN001
        return {"settings": self}
