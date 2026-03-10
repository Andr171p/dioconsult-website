from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.blocks import (
    CharBlock, RichTextBlock, StructBlock, ListBlock, ChoiceBlock, PageChooserBlock
)
from wagtail.images.blocks import ImageChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from wagtail.snippets.models import register_snippet
from modelcluster.models import ClusterableModel
from django.utils import timezone


# ========================================
# ДИНАМИЧЕСКИЕ КАТЕГОРИИ 
# ========================================
@register_snippet
class ProductCategory(ClusterableModel):
    name = models.CharField(max_length=100, verbose_name="Название")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="Slug")

    panels = [
        FieldPanel('name'),
        FieldPanel('slug'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория продукта"
        verbose_name_plural = "Категории продуктов"


# ========================================
# БЛОКИ ДЛЯ STREAMFIELD
# ========================================

class HeroBlock(StructBlock):
    title = CharBlock(required=True, label="Заголовок Hero")
    subtitle = CharBlock(required=True, label="Подзаголовок Hero")
    image = ImageChooserBlock(required=True, label="Изображение Hero")
    button_text = CharBlock(required=False, label="Текст кнопки")
    button_link = PageChooserBlock(
        required=False, 
        label="Ссылка кнопки",
        target_model='wagtailcore.Page'  # Добавлено!
    )

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


# ========================================
# СТРАНИЦА-ПРОДУКТ: ProductPage
# ========================================
class ProductPage(Page):
    category = models.ForeignKey(
        'pages.ProductCategory',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='products',
        verbose_name="Категория"
    )
    price = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    description = RichTextField(blank=True, features=['italic', 'ol', 'ul', 'link'])
    buy_link = models.URLField(blank=True)
    hero_image = models.ForeignKey('wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    
    date = models.DateField("Дата публикации", default=timezone.now)
    headline = models.CharField("Заголовок", max_length=255, default="Заголовок продукта")
    intro = models.TextField("Краткое описание", blank=True, help_text="1-3 предложения для анонса")

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
                FieldPanel('category'),
                FieldPanel('price'),
                FieldPanel('description'),
                FieldPanel('buy_link'),
                FieldPanel('hero_image'),
                FieldPanel('date'),
                FieldPanel('headline'),
                FieldPanel('intro'),
            ],
            heading="Основная информация",
        ),
        MultiFieldPanel([
            FieldPanel('content'),
        ], heading="Блоки страницы"),
    ]

    parent_page_types = ['pages.ProgramsPage']
    subpage_types = []

    def get_context(self, request):
        context = super().get_context(request)
        context["other_products"] = (
            ProductPage.objects.live().exclude(id=self.id).order_by("-date")[:3]
        )
        return context

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"


# ========================================
# СТРАНИЦА-КАТАЛОГ: ProgramsPage
# ========================================
class ProgramsPage(Page):
    intro = RichTextField(blank=True, features=['italic'], verbose_name="Введение")

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]

    subpage_types = ['pages.ProductPage']
    parent_page_types = ['home.HomePage']

    class Meta:
        verbose_name = "Лента Программ"

    def get_context(self, request):
        context = super().get_context(request)

        products = ProductPage.objects.live().order_by('title')
        category_slug = request.GET.get('category')

        if category_slug and category_slug != 'all':
            products = products.filter(category__slug=category_slug)

        # Пагинация
        paginator = Paginator(products, 9)
        page = request.GET.get('page')
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)

        categories = ProductCategory.objects.all()

        context.update({
            'products': products,
            'categories': categories,
            'selected_category': category_slug or 'all',
        })
        return context