# pages/models/about.py

from django.db import models

from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import StreamField
from wagtail.search import index

from wagtail.blocks import (
    CharBlock,
    RichTextBlock,
    StructBlock,
    ListBlock,
    PageChooserBlock,
    ChoiceBlock,
    IntegerBlock,
)
from wagtail.images.blocks import ImageChooserBlock
from wagtail.embeds.blocks import EmbedBlock


# ────────────────────────────────────────────────
# Блоки достижений и глобального присутствия
# (определены здесь, чтобы избежать циклических импортов)
# ────────────────────────────────────────────────

class MainAchievementBlock(StructBlock):
    icon = ImageChooserBlock(required=False, label="Иконка")
    value = IntegerBlock(default=0, label="Числовое значение")
    suffix = CharBlock(max_length=10, blank=True, default="+", label="Суффикс (например, '+' или '%')")
    label = CharBlock(max_length=100, label="Краткое название")
    description = RichTextBlock(blank=True, label="Описание достижения")

    class Meta:
        icon = "tick"
        label = "Основное достижение"


class AdditionalAchievementBlock(StructBlock):
    value = CharBlock(max_length=10, blank=True, label="Числовое значение или текст")
    title = CharBlock(max_length=100, blank=True, label="Заголовок достижения")
    description = RichTextBlock(blank=True, label="Описание достижения")

    class Meta:
        icon = "plus"
        label = "Дополнительное достижение"


class GlobalPresenceBlock(StructBlock):
    title = CharBlock(required=True, default="Глобальное присутствие", label="Заголовок")
    description = RichTextBlock(
        features=["bold", "italic", "ol", "ul", "link", "superscript"],
        required=False,
        label="Описание"
    )
    image = ImageChooserBlock(
        required=True,
        label="Изображение для локации",
        help_text="Рекомендуемый размер: квадратное или 1x1"
    )

    class Meta:
        icon = "globe"
        label = "Глобальное присутствие"


# ────────────────────────────────────────────────
# Все остальные блоки страницы
# ────────────────────────────────────────────────

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
    title = CharBlock(required=False, label="Заголовок блока", default="Результаты")
    items = ListBlock(ResultItemBlock(), label="Список результатов")

    class Meta:
        icon = 'tick'
        label = "Блок результатов"


class DescriptionBlock(StructBlock):
    title = CharBlock(required=False, label="Заголовок блока", default="Описание проекта")
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
        choices=[('left', 'Слева'), ('right', 'Справа')],
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


class CTABlock(StructBlock):
    title = CharBlock(required=True, label="Заголовок CTA")
    description = RichTextBlock(required=True, label="Описание CTA")
    button_text = CharBlock(required=True, label="Текст кнопки")
    button_link = PageChooserBlock(required=False, label="Ссылка")

    class Meta:
        icon = "plus"
        label = "CTA"


# ────────────────────────────────────────────────
# Модель страницы "О компании"
# ────────────────────────────────────────────────

class AboutPage(Page):
    """Страница 'О компании' с современными блоками"""

    achievements = StreamField(
        [
            ("main_achievement", MainAchievementBlock()),
            ("additional_achievement", AdditionalAchievementBlock()),
        ],
        blank=True,
        use_json_field=True,
        verbose_name="Достижения",
    )

    global_presence = StreamField(
        [
            ("presence", GlobalPresenceBlock()),
        ],
        blank=True,
        use_json_field=True,
        verbose_name="Глобальное присутствие",
        max_num=1,
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
        ('cta', CTABlock()),
    ], blank=True, use_json_field=True, verbose_name="Блоки страницы")

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('content'),
        ], heading="Основные блоки страницы"),
        MultiFieldPanel([
            FieldPanel('achievements'),
        ], heading="Достижения"),
        MultiFieldPanel([
            FieldPanel('global_presence'),
        ], heading="Глобальное присутствие"),
    ]

    search_fields = Page.search_fields + [
        index.SearchField("content"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        
        context["main_achievements"] = [
            block for block in self.achievements 
            if block.block_type == "main_achievement"
        ]
        context["additional_achievements"] = [
            block for block in self.achievements 
            if block.block_type == "additional_achievement"
        ]
        
        # Ленивый импорт HomePage внутри метода (безопасно)
        from home.models import HomePage
        home_page = HomePage.objects.live().first()
        if home_page:
            context['home_global_presence'] = home_page.global_presence
            
        return context

    class Meta:
        verbose_name = "Страница 'О компании'"
        verbose_name_plural = "Страницы 'О компании'"