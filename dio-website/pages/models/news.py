from django.db import models
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.search import index
from django.utils import timezone
from wagtail import blocks
from wagtail.blocks import RichTextBlock
from wagtail.images.blocks import ImageChooserBlock
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from wagtail.blocks import URLBlock
from wagtail.embeds.blocks import EmbedBlock

NEWS_CATEGORY_CHOICES = [
    ("company", "Новости компании"),
    ("tech", "Технологии"),
    ("projects", "Проекты"),
    ("events", "События"),
    ("awards", "Награды"),
]

class NewsPage(Page):
    """Страница отдельной новости"""

    date = models.DateField("Дата публикации", default=timezone.now)
    read_time = models.PositiveIntegerField(
        "Время чтения (мин)",
        default=1,
        help_text="Примерное время чтения статьи в минутах"
    )
    category = models.CharField(
        max_length=100,
        choices=NEWS_CATEGORY_CHOICES,
        default="company",
        verbose_name="Категория",
    )
    headline = models.CharField(
        "Заголовок", max_length=255, default="Заголовок новости"
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
    media_content = StreamField([
        ('image', blocks.StructBlock([
            ('image', ImageChooserBlock(required=True)),
            ('caption', RichTextBlock(required=False)),
        ], label="Изображение")),
        ('video', blocks.StructBlock([
            ('video_url', URLBlock(required=True, help_text="Ссылка на YouTube, Vimeo и т.д.")),
            ('caption', RichTextBlock(required=False)),
        ], label="Видео")),
        ('embed', EmbedBlock(
            help_text="Вставьте ссылку на видео (YouTube, Vimeo и т.д.)",
            label="Видео (автовставка)"
        )),
    ], blank=True, use_json_field=True, verbose_name="Медиа контент")

    content = RichTextField("Содержание", blank=True)
    gallery = StreamField([
        ('image', blocks.StructBlock([
            ('image', ImageChooserBlock(required=True)),
            ('caption', RichTextBlock(required=False)),
        ], label="Изображение галереи")),
    ], blank=True, use_json_field=True, verbose_name="Галерея")

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("date"),
                FieldPanel("read_time"),
                FieldPanel("category"),
                FieldPanel("headline"),
                FieldPanel("intro"),
                FieldPanel("image"),
            ],
            heading="Основная информация",
        ),
        FieldPanel("content"),
        
        FieldPanel("gallery"),
    ]

    search_fields = Page.search_fields + [
        index.SearchField("headline"),
        index.SearchField("intro"),
        index.SearchField("content"),
    ]

    parent_page_types = ['pages.NewsIndexPage']
    subpage_types = []

    def get_context(self, request):
        context = super().get_context(request)
        context["other_news"] = (
            NewsPage.objects.live().exclude(id=self.id).order_by("-date")[:3]
        )
        return context

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"

class NewsIndexPage(Page):
    """Главная страница новостей"""

    intro = RichTextField("Введение", features=[ "italic", "link"], blank=True)
    items_per_page = models.PositiveIntegerField("Новостей на странице", default=9)

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        FieldPanel("items_per_page"),
    ]

    subpage_types = ['pages.NewsPage']
    parent_page_types = ['home.HomePage']

    def get_context(self, request):
        context = super().get_context(request)
        news = NewsPage.objects.live().order_by("-date")
        category = request.GET.get("category")
        if category:
            news = news.filter(category=category)
        context["current_category"] = category

        paginator = Paginator(news, self.items_per_page)
        page = request.GET.get("page")
        try:
            news = paginator.page(page)
        except PageNotAnInteger:
            news = paginator.page(1)
        except EmptyPage:
            news = paginator.page(paginator.num_pages)

        context["news"] = news
        context["NEWS_CATEGORY_CHOICES"] = NEWS_CATEGORY_CHOICES
        return context

    class Meta:
        verbose_name = "Лента новостей"
        verbose_name_plural = "Ленты новостей"

class NewsBlock(blocks.StructBlock):
    """Блок для отображения новостей на главной странице"""

    title = blocks.CharBlock(
        max_length=100, required=True, label="Заголовок секции новостей"
    )
    show_count = blocks.IntegerBlock(
        default=3, min_value=1, max_value=12, label="Количество новостей для показа"
    )

    class Meta:
        icon = "doc-full"
        label = "Блок новостей"
