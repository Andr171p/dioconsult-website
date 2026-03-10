# career/models.py
from django.db import models
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import StreamField
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.blocks import (
    CharBlock, RichTextBlock, StructBlock, ListBlock, 
    ChoiceBlock
)
from wagtail.embeds.blocks import EmbedBlock

class HeroBlock(StructBlock):
    title = CharBlock(default="Присоединяйся к DIO", label="Заголовок")
    subtitle = CharBlock(required=False, label="Подзаголовок")
    image = ImageChooserBlock(required=False, label="Изображение")
    cta_text = CharBlock(default="Смотреть вакансии", label="Текст кнопки")
    cta_scroll = blocks.BooleanBlock(default=True, help_text="Прокрутка к вакансиям")

    class Meta:
        icon = "image"
        label = "Hero"

class TextBlock(StructBlock):
    title = CharBlock(default="О компании", label="Заголовок")
    content = RichTextBlock(required=False, label="Контент")
    image = ImageChooserBlock(required=False, label="Изображение")

    class Meta:
        icon = "doc-full"
        label = "Текстовая секция"



class VacanciesListBlock(StructBlock):
    title = CharBlock(default="Открытые вакансии", label="Заголовок")

    class Meta:
        icon = "user"
        label = "Список вакансий"

class FormBlock(StructBlock):
    title = CharBlock(default="Хочешь к нам?", label="Заголовок")
    description = blocks.TextBlock(required=False, label="Описание")

    class Meta:
        icon = "mail"
        label = "Форма"

class OfficeBlock(StructBlock):
    title = CharBlock(default="Наш офис", label="Заголовок")
    address = CharBlock(required=False, label="Адрес")

    class Meta:
        icon = "home"
        label = "Офис"

class WhatWeDoBlock(StructBlock):
    title = CharBlock(required=True, label="Заголовок")
    description = RichTextBlock(required=True, label="Описание")
    image = ImageChooserBlock(required=True, label="Изображение")
    image_position = ChoiceBlock(
        choices=[
            ('left', 'Слева'),
            ('right', 'Справа'),
        ],
        default='left',
        label="Позиция изображения"
    )

    class Meta:
        icon = "edit"
        label = "Что мы делаем"

class BenefitItemBlock(StructBlock):
    title = CharBlock(required=True, label="Название преимущества")
    description = RichTextBlock(required=True, label="Описание")
    icon = ImageChooserBlock(required=False, label="Иконка")

    class Meta:
        icon = 'tick'
        label = "Преимущество"

class BenefitsBlock(StructBlock):
    title = CharBlock(required=False, label="Заголовок блока", default="Ключевые преимущества")
    items = ListBlock(BenefitItemBlock(), label="Список преимуществ")

    class Meta:
        icon = 'plus'
        label = "Блок преимуществ"

class ProcessItemBlock(StructBlock):
    title = CharBlock(required=True, label="Название этапа")
    description = RichTextBlock(required=True, label="Описание этапа")

    class Meta:
        icon = 'list-ul'
        label = "Этап процесса"

class ProcessBlock(StructBlock):
    title = CharBlock(required=False, label="Заголовок блока", default="Как мы работаем")
    items = ListBlock(ProcessItemBlock(), label="Этапы работы")

    class Meta:
        icon = 'cog'
        label = "Процесс работы"

class GalleryBlock(StructBlock):
    title = CharBlock(required=False, label="Заголовок галереи")
    images = ListBlock(ImageChooserBlock(), label="Изображения")

    class Meta:
        icon = "image"
        label = "Галерея изображений"

class VideoBlock(StructBlock):
    title = CharBlock(required=False, label="Заголовок видео")
    video = EmbedBlock(required=True, label="Встраиваемое видео")

    class Meta:
        icon = "media"
        label = "Видео"

class AccordionItemBlock(StructBlock):
    question = CharBlock(required=True, label="Вопрос/Заголовок")
    answer = RichTextBlock(required=True, label="Ответ/Описание")

    class Meta:
        icon = "help"
        label = "Элемент аккордеона"

class AccordionBlock(StructBlock):
    title = CharBlock(required=True, label="Заголовок аккордеона")
    items = ListBlock(AccordionItemBlock(), label="Элементы аккордеона")

    class Meta:
        icon = "list-ul"
        label = "Аккордеон (FAQ/Детали)"


class CareerPage(Page):
    template = "career/career_page.html"

    content = StreamField([
        ('hero', HeroBlock()),
        ('text_section', TextBlock()),
        ('what_we_do', WhatWeDoBlock()),
        ('benefits', BenefitsBlock()),
        ('process', ProcessBlock()),
        ('vacancies_list', VacanciesListBlock()),
        ('gallery', GalleryBlock()),
        ('video', VideoBlock()),
        ('accordion', AccordionBlock()),
        ('form', FormBlock()),
        ('office', OfficeBlock()),
    ], use_json_field=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("content"),
    ]

    subpage_types = ['career.CareerVacancyPage']
    parent_page_types = ['home.HomePage']
    
    class Meta:
        verbose_name = "Страница 'Карьера'"
        verbose_name_plural = "Страницы 'Карьера'"

class CareerVacancyPage(Page):
    template = "career/career_vacancy_page.html"

    department = models.CharField(max_length=100, default="Разработка")
    salary = models.CharField(max_length=100, blank=True, help_text="Например: от 150 000 ₽")
    location = models.CharField(max_length=100, default="Тюмень")
    work_format = models.CharField(
        max_length=50,
        choices=[("office", "Офис"), ("remote", "Удалённо"), ("hybrid", "Гибрид")],
        default="office"
    )
    
    hero_image = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True, on_delete=models.SET_NULL, related_name='+'
    )

    content = StreamField([
        ("text_section", TextBlock()),
        ("what_we_do", WhatWeDoBlock()),
        ("benefits", BenefitsBlock()),
        ("process", ProcessBlock()),
        ("gallery", GalleryBlock()),
        ("video", VideoBlock()),
        ("accordion", AccordionBlock()),
    ], use_json_field=True, blank=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel("title"),
            FieldPanel("department"),
            FieldPanel("salary"),
            FieldPanel("location"),
            FieldPanel("work_format"),
            FieldPanel("hero_image"),
        ], heading="Основная информация", classname="collapsible"),
        FieldPanel("content"),
    ]

    parent_page_types = ["career.CareerPage"]
    subpage_types = []

    class Meta:
        verbose_name = "Вакансия"
        verbose_name_plural = "Вакансии"
