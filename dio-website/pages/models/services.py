from django.db import models
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.search import index
from django.utils import timezone
from wagtail.blocks import (
    CharBlock, RichTextBlock, StructBlock, ListBlock, PageChooserBlock, ChoiceBlock
)
from wagtail.images.blocks import ImageChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail import blocks
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

SERVICE_CATEGORY_CHOICES = [
    ("consulting", "Консультации"),
    ("development", "Разработка"),
    ("design", "Дизайн"),
    ("support", "Поддержка"),
    ("training", "Обучение"),
    ("1_c", "1С"),
]



class HeroBlock(StructBlock):
    title = CharBlock(required=True, label="Заголовок Hero")
    subtitle = CharBlock(required=True, label="Подзаголовок Hero")
    image = ImageChooserBlock(required=True, label="Изображение Hero")
    button_text = CharBlock(required=False, label="Текст кнопки")
    button_link = PageChooserBlock(required=False, label="Ссылка кнопки")

    class Meta:
        icon = "image"
        label = "Hero"

class TextBlock(StructBlock):
    content = RichTextBlock(
        features=['h2', 'h3', 'bold', 'italic', 'link', 'ol', 'ul', 'blockquote'],
        label="Текст"
    )

    class Meta:
        icon = "doc-full"
        label = "Текстовая секция"

class ResultItemBlock(StructBlock):
    text = RichTextBlock(
        label="Текст результата",
        features=['bold', 'italic', 'link'],
        required=True
    )

    class Meta:
        icon = 'success'
        label = "Элемент результата"

class ResultsBlock(StructBlock):
    title = CharBlock(
        required=False, 
        label="Заголовок блока",
        default="Результаты"
    )
    items = ListBlock(
        ResultItemBlock(),
        label="Список результатов"
    )

    class Meta:
        icon = 'tick'
        label = "Блок результатов"

class DescriptionBlock(StructBlock):
    title = CharBlock(
        required=False, 
        label="Заголовок блока",
        default="Описание проекта"
    )
    content = RichTextBlock(
        label="Описание",
        features=['bold', 'italic', 'link', 'h2', 'h3', 'h4', 'ol', 'ul', 'image', 'embed', 'code', 'blockquote', 'hr', 'document-link', 'superscript', 'strikethrough'],
        required=True
    )

    class Meta:
        icon = 'doc-full'
        label = "Описание проекта"

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


class GalleryBlock(StructBlock):
    title = CharBlock(required=False, label="Заголовок галереи")
    images = ListBlock(ImageChooserBlock(), label="Изображения")

    class Meta:
        icon = "image"
        label = "Галерея изображений"

class VideoBlock(StructBlock):
    title = CharBlock(required=False, label="Заголовок видео")
    video = EmbedBlock(required=True, label="Встраиваемое видео (YouTube, Vimeo и т.д.)")

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

class TechnologyItemBlock(StructBlock):
    name = CharBlock(required=True, label="Название технологии")
    icon = ImageChooserBlock(required=True, label="Логотип/Иконка")

    class Meta:
        icon = 'code'
        label = "Технология"

class TechnologiesBlock(StructBlock):
    title = CharBlock(required=False, label="Заголовок блока", default="Технологии и инструменты")
    items = ListBlock(TechnologyItemBlock(), label="Список технологий")

    class Meta:
        icon = 'site'
        label = "Технологии"



class SingleServicePage(Page):
    date = models.DateField("Дата публикации", default=timezone.now)
    category = models.CharField(
        max_length=100,
        choices=SERVICE_CATEGORY_CHOICES,
        default="consulting",
        verbose_name="Категория",
    )
    headline = models.CharField(
        "Заголовок", max_length=255, default="Заголовок услуги"
    )
    intro = models.TextField(
        "Краткое описание", blank=True, help_text="1-3 предложения для анонса"
    )
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Изображение",
    )
    content = StreamField([
        ('hero', HeroBlock()),
        ('text', TextBlock()),
        ('what_we_do', WhatWeDoBlock()),
        ('description', DescriptionBlock()), 
        ('results', ResultsBlock()), 
        ('benefits', BenefitsBlock()),  
        ('process', ProcessBlock()),    
        ('technologies', TechnologiesBlock()), 
        ('gallery', GalleryBlock()),
        ('video', VideoBlock()),
        ('accordion', AccordionBlock()),
    ], blank=True, use_json_field=True, verbose_name="Блоки страницы")

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("date"),
                FieldPanel("category"),
                FieldPanel("headline"),
                FieldPanel("intro"),
                FieldPanel("image"),
            ],
            heading="Основная информация",
        ),
        MultiFieldPanel([
            FieldPanel('content'),
        ], heading="Блоки страницы"),
    ]

    search_fields = Page.search_fields + [
        index.SearchField("headline"),
        index.SearchField("intro"),
        index.SearchField("content"),
    ]

    parent_page_types = ["pages.ServiceIndexPage"]   
    subpage_types = []

    def get_context(self, request):
        context = super().get_context(request)
        context["other_services"] = (
            SingleServicePage.objects.live().exclude(id=self.id).order_by("-date")[:3]
        )
        return context

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"

class ServiceIndexPage(Page):
    intro = RichTextField("Введение", features=[ "italic", "link"], blank=True)
    items_per_page = models.PositiveIntegerField("Услуг на странице", default=9)

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        FieldPanel("items_per_page"),
    ]

    subpage_types = ['pages.SingleServicePage']
    parent_page_types = ['home.HomePage']

    def get_context(self, request):
        context = super().get_context(request)
        
        services = SingleServicePage.objects.live().order_by("-date")

        category = request.GET.get("category")

        if category and category in dict(SERVICE_CATEGORY_CHOICES):
            services = services.filter(category=category)

        context["current_category"] = category if category and category in dict(SERVICE_CATEGORY_CHOICES) else None

        paginator = Paginator(services, self.items_per_page)
        page = request.GET.get("page")
        try:
            services = paginator.page(page)
        except PageNotAnInteger:
            services = paginator.page(1)
        except EmptyPage:
            services = paginator.page(paginator.num_pages)

        context["services"] = services
        context["SERVICE_CATEGORY_CHOICES"] = SERVICE_CATEGORY_CHOICES
        return context

    class Meta:
        verbose_name = "Лента услуг"
        verbose_name_plural = "Ленты услуг"

class ServiceBlock(blocks.StructBlock):
    title = blocks.CharBlock(
        max_length=100, required=True, label="Заголовок секции услуг"
    )
    show_count = blocks.IntegerBlock(
        default=3, min_value=1, max_value=12, label="Количество услуг для показа"
    )

    class Meta:
        icon = "doc-full"
        label = "Блок услуг"

