from typing import ClassVar

from config.settings.dev import SITE_URL as SITE_DOMAIN
from django.db import models
from notification.utils import create_admin_notification
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.models import Page
from wagtail.search import index


class VacancyPage(Page):
    responsibilities = models.TextField(verbose_name="Обязанности")
    requirements = models.TextField(verbose_name="Требования")
    conditions = models.TextField(verbose_name="Условия")

    content_panels: ClassVar[list] = [
        *Page.content_panels,
        MultiFieldPanel([
            FieldPanel("responsibilities"),
            FieldPanel("requirements"),
            FieldPanel("conditions"),
        ]),
    ]

    search_fields: ClassVar[list] = [
        *Page.search_fields,
        index.SearchField("title"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        from ..forms.vacancy import VacancyForm

        context["form"] = VacancyForm()
        return context

    class Meta:
        verbose_name = "Вакансия"
        verbose_name_plural = "Вакансии"


class Vacancy(models.Model):
    title = models.CharField(verbose_name="Вакансия",max_length=50)
    name = models.CharField(verbose_name="Имя",max_length=50)
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    resume = models.FileField(
        upload_to="resumes/%Y/%m/%d/",
        verbose_name="Резюме",
        null=True,
        blank=True,
    )
    resume_link = models.URLField(
        verbose_name="Ссылка для скачивания резюме",
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    is_processed = models.BooleanField(default=False, verbose_name="Просмотрено")

    def __str__(self) -> str:
        return f"{self.name} - {self.title}"

    def save(self, *args, **kwargs) -> None:
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if self.resume:
            self.resume_link = f"{SITE_DOMAIN}/vacancy/resume/download/{self.id}/"
        else:
            self.resume_link = None

        super().save(update_fields=["resume_link"])

        if is_new:
            create_admin_notification(
                title="Новый отклик на вакансию",
                message=f"Резюме от {self.name} на вакансию {self.title}",
                url=f"{SITE_DOMAIN}/admin/snippets/vacancy/vacancy/edit/{self.id}/",
            )

    class Meta:
        verbose_name = "Отклик на вакансию"
        verbose_name_plural = "Отклики на вакансии"
