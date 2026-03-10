from wagtail import blocks
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock


class FeedbackFormBlock(blocks.StructBlock):
    """Блок формы обратной связи"""
    form_title = blocks.CharBlock(
        required=False, default="Свяжитесь с нами", label="Заголовок формы"
    )
    form_description = blocks.TextBlock(
        required=False, label="Описание формы"
    )
    success_message = blocks.CharBlock(
        required=False,
        default="Спасибо! Ваше сообщение отправлено.",
        label="Сообщение об успешной отправке"
    )

    class Meta:
        icon = "form"
        label = "Форма обратной связи"


class ContactsBlock(blocks.StructBlock):
    """Блок контактов компании"""
    section_title = blocks.CharBlock(
        required=False,
        default="Контакты",
        label="Заголовок секции"
    )
    show_map = blocks.BooleanBlock(
        required=False,
        default=True,
        label="Показывать карту"
    )
    map_embed = EmbedBlock(
        required=False,
        label="Код embed карты",
        help_text="Вставьте embed код карты из Yandex Maps, Google Maps, ..."
    )
    contact_items = blocks.ListBlock(
        blocks.PageChooserBlock(
            page_type=None, label="Контакты"
        ),
        required=False,
        label="Выбранные контакты"
    )

    class Meta:
        icon = "group"
        label = "Блок контактов"


class HeroCarouselSlideBlock(blocks.StructBlock):
    """Блок для слайда карусели в секции hero"""
    headline = blocks.CharBlock(max_length=100, required=True, label="Заголовок")
    subheadline = blocks.CharBlock(max_length=250, required=False, label="Подзаголовок")
    background_image = ImageChooserBlock(required=True, label="Фоновое изображение", help_text="Рекомендуемый размер: 1920x1080px")
    button_text = blocks.CharBlock(required=True, default="Подробнее", label="Текст кнопки")
    button_link = blocks.URLBlock(required=True, label="Ссылка кнопки")

    class Meta:
        icon = "image"
        template = "home/blocks/hero_carousel_slide.html"

class HeroCarouselBlock(blocks.StreamBlock):
    """Карусельная секция hero"""
    slide = HeroCarouselSlideBlock(label="Слайд")

    class Meta:
        icon = "carousel"
        template = "home/blocks/hero_carousel.html"
