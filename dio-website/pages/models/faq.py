from django.db import models
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import StreamField
from wagtail import blocks

class FAQPage(Page):
    """Отдельная страница со множеством вопросов"""
    question = blocks.CharBlock(
        max_length=255,
        required=True,
        label="Вопрос"
    )
    
    answer = blocks.RichTextBlock(
        required=True,
        label="Ответ",
        features=['bold', 'italic', 'link', 'ol', 'ul']
    )
    eyebrow = models.CharField(
        max_length=255, 
        blank=True,
        verbose_name="Надзаголовок"
    )
    
    heading = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Основной заголовок"
    )
    
    subheading = models.TextField(
        blank=True,
        verbose_name="Подзаголовок"
    )

    faq_items = StreamField(
        [
            ("faq", blocks.StructBlock([
                ("question", blocks.CharBlock(
                    max_length=255,
                    required=True,
                    label="Вопрос"
                )),
                ("answer", blocks.RichTextBlock(
                    required=True,
                    label="Ответ",
                    features=['bold', 'italic', 'link', 'ol', 'ul']
                ))
            ], icon="help", label="Вопрос-ответ"))
        ],
        blank=True,
        use_json_field=True,
        verbose_name="Вопросы и ответы"
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("eyebrow"),
                FieldPanel("heading"),
                FieldPanel("subheading"),
            ],
            heading="Заголовок секции",
        ),
        FieldPanel("faq_items"),
    ]

    template = "faq/faqitem.html"

    class Meta:
        verbose_name = "Страница FAQ"
        verbose_name_plural = "Страницы FAQ"
