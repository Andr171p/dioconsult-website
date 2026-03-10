# home/models.py или contact/models.py
from django.db import models
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail import blocks
from wagtail.documents.blocks import DocumentChooserBlock


class ContactPage(Page):
    """Страница контактов с полным соответствием требованиям №511"""
    
    # --- Блок 1: Контактная информация ---
    address = models.TextField(
        "Адрес",
        help_text="Полный адрес с индексом",
        blank=True
    )
    phone = models.CharField(
        "Телефон", 
        max_length=20,
        blank=True
    )
    email = models.EmailField(
        "Email",
        blank=True
    )
    work_hours = models.CharField(
        "Режим работы", 
        max_length=200,
        blank=True
    )
    
    # --- Блок 2: Юридические данные ---
    legal_name = models.CharField(
        "Полное наименование",
        max_length=255,
        blank=True
    )
    inn = models.CharField(
        "ИНН", 
        max_length=12,
        blank=False  # Обязательное поле
    )
    ogrn = models.CharField(
        "ОГРН", 
        max_length=15,
        blank=True
    )
    kpp = models.CharField(
        "КПП", 
        max_length=9,
        blank=True
    )
    okpo = models.CharField(
        "ОКПО", 
        max_length=10,
        blank=True
    )
    
    # --- Блок 3: Коды деятельности ---
    okved_codes = RichTextField(
        "Коды ОКВЭД",
        features=['bold', 'italic', 'ol', 'ul'],
        blank=True
    )
    
    # --- Блок 4: ИТ-деятельность (Приказ №449) ---
    it_activity_codes = RichTextField(
        "Коды ИТ-деятельности (Приказ Минцифры №449)",
        features=['bold', 'italic', 'ol', 'ul'],
        blank=True
    )
    
    # --- Блок 5: Информация о стоимости ---
    price_info = RichTextField(
        "Информация о стоимости услуг",
        features=['bold', 'italic', 'ol', 'ul'],
        blank=True
    )
    
    # --- Блок 6: Правообладание ПО ---
    software_rights = RichTextField(
        "Правообладание программным обеспечением",
        features=['bold', 'italic', 'ol', 'ul', 'h3', 'h4'],
        blank=True
    )
    
    # --- Блок 7: Технологии ---
    technologies = RichTextField(
        "Технологический стек",
        features=['bold', 'italic'],
        blank=True
    )
    
    # --- Блок 8: Карта ---
    map_embed_code = models.TextField(
        "Код встраивания карты",
        blank=True
    )
    
    # --- Блок 9: Дополнительная информация ---
    additional_info = RichTextField(
        "Дополнительная информация",
        features=['bold', 'italic', 'ol', 'ul', 'h3'],
        blank=True
    )
    
    # --- StreamField для динамических блоков ---
    dynamic_blocks = StreamField([
        ('heading', blocks.StructBlock([
            ('title', blocks.CharBlock(label="Заголовок")),
            ('subtitle', blocks.TextBlock(label="Подзаголовок", required=False)),
        ], icon='title', label="Заголовок раздела")),
        
        ('info_card', blocks.StructBlock([
            ('title', blocks.CharBlock(label="Заголовок карточки")),
            ('content', blocks.RichTextBlock(label="Содержание")),
            ('icon_class', blocks.CharBlock(
                label="Класс иконки", 
                required=False,
                help_text="Например: fas fa-phone, fas fa-envelope"
            )),
        ], icon='doc-full', label="Информационная карточка")),
        
        ('technology_item', blocks.StructBlock([
            ('name', blocks.CharBlock(label="Название технологии")),
            ('description', blocks.TextBlock(label="Описание", required=False)),
        ], icon='code', label="Технология")),
        
        ('legal_document', blocks.StructBlock([
            ('title', blocks.CharBlock(label="Название документа")),
            ('content', blocks.RichTextBlock(label="Содержание")),
            ('file', DocumentChooserBlock(label="Файл", required=False)),
        ], icon='doc-full-inverse', label="Юридический документ")),
        
        ('contact_method', blocks.StructBlock([
            ('type', blocks.ChoiceBlock(choices=[
                ('phone', 'Телефон'),
                ('email', 'Email'),
                ('whatsapp', 'WhatsApp'),
                ('telegram', 'Telegram'),
                ('viber', 'Viber'),
            ], label="Тип контакта")),
            ('value', blocks.CharBlock(label="Значение")),
            ('description', blocks.CharBlock(label="Описание", required=False)),
        ], icon='user', label="Способ связи")),
        
        ('social_link', blocks.StructBlock([
            ('platform', blocks.ChoiceBlock(choices=[
                ('vk', 'ВКонтакте'),
                ('telegram', 'Telegram'),
                ('whatsapp', 'WhatsApp'),
                ('viber', 'Viber'),
                ('skype', 'Skype'),
            ], label="Платформа")),
            ('url', blocks.URLBlock(label="Ссылка")),
            ('text', blocks.CharBlock(label="Текст ссылки", required=False)),
        ], icon='site', label="Социальная сеть")),
        
        ('map_block', blocks.StructBlock([
            ('title', blocks.CharBlock(label="Заголовок карты")),
            ('embed_code', blocks.TextBlock(label="Код для вставки карты")),
            ('description', blocks.TextBlock(label="Описание", required=False)),
        ], icon='site', label="Карта")),
        
        ('pricing_table', blocks.StructBlock([
            ('title', blocks.CharBlock(label="Заголовок таблицы")),
            ('services', blocks.ListBlock(
                blocks.StructBlock([
                    ('service_name', blocks.CharBlock(label="Услуга")),
                    ('description', blocks.TextBlock(label="Описание", required=False)),
                    ('price', blocks.CharBlock(label="Стоимость")),
                ], label="Услуга")
            )),
        ], icon='table', label="Таблица цен")),
        
        ('accordion', blocks.StructBlock([
            ('title', blocks.CharBlock(label="Заголовок аккордеона")),
            ('items', blocks.ListBlock(
                blocks.StructBlock([
                    ('question', blocks.CharBlock(label="Вопрос")),
                    ('answer', blocks.RichTextBlock(label="Ответ")),
                ], label="Элемент")
            )),
        ], icon='list-ul', label="Аккордеон FAQ")),
    ], 
    block_counts={
        'heading': {'min_num': 0, 'max_num': 5},
        'info_card': {'min_num': 0, 'max_num': 10},
        'technology_item': {'min_num': 0, 'max_num': 20},
        'contact_method': {'min_num': 0, 'max_num': 10},
        'social_link': {'min_num': 0, 'max_num': 10},
        'map_block': {'min_num': 0, 'max_num': 1},
        'pricing_table': {'min_num': 0, 'max_num': 3},
        'accordion': {'min_num': 0, 'max_num': 2},
    },
    use_json_field=True, 
    blank=True, 
    verbose_name="Динамические блоки")
    
    # --- Панели админки ---
    content_panels = Page.content_panels + [
        # Панель 1: Основная контактная информация
        MultiFieldPanel([
            FieldPanel('address'),
            FieldPanel('phone'),
            FieldPanel('email'),
            FieldPanel('work_hours'),
        ], heading="Основная контактная информация", classname="collapsible"),
        
        # Панель 2: Юридические реквизиты
        MultiFieldPanel([
            FieldPanel('legal_name'),
            FieldPanel('inn'),
            FieldPanel('ogrn'),
            FieldPanel('kpp'),
            FieldPanel('okpo'),
        ], heading="Юридические реквизиты", classname="collapsible"),
        
        # Панель 3: Информация для ИТ-аккредитации
        MultiFieldPanel([
            FieldPanel('okved_codes'),
            FieldPanel('it_activity_codes'),
            FieldPanel('price_info'),
            FieldPanel('software_rights'),
            FieldPanel('technologies'),
        ], heading="Информация для ИТ-аккредитации (№511)", classname="collapsible"),
        
        # Панель 4: Карта
        MultiFieldPanel([
            FieldPanel('map_embed_code'),
        ], heading="Карта", classname="collapsible"),
        
        # Панель 5: Дополнительная информация
        MultiFieldPanel([
            FieldPanel('additional_info'),
        ], heading="Дополнительная информация", classname="collapsible"),
        
        # Панель 6: Динамические блоки (полная свобода через админку)
        MultiFieldPanel([
            FieldPanel('dynamic_blocks'),
        ], heading="Динамические блоки контента", classname="collapsible collapsed"),
    ]
    
    # --- Настройки отображения в админке ---
    promote_panels = Page.promote_panels + [
        MultiFieldPanel([
            FieldPanel('slug'),
            FieldPanel('seo_title'),
            FieldPanel('search_description'),
        ], heading="SEO настройки")
    ]
    
    # --- Шаблон ---
    template = "contact/contact_page.html"
    
    # --- Контекст ---
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        
        # Группировка технологий для удобного отображения
        if self.technologies:
            context['tech_list'] = [tech.strip() for tech in self.technologies.split(',')]
        else:
            context['tech_list'] = []
            
        return context
    
    class Meta:
        verbose_name = "Страница контактов"
        verbose_name_plural = "Страницы контактов"
