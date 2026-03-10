from django.db import models
from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.images.blocks import ImageChooserBlock


class CertificateBlock(blocks.StructBlock):
    title = blocks.CharBlock(max_length=200, label="Название сертификата")
    issuer = blocks.CharBlock(max_length=200, label="Кем выдан")
    issue_date = blocks.DateBlock(label="Дата выдачи")
    thumbnail = ImageChooserBlock(required=False, label="Превью сертификата")
    document = DocumentChooserBlock(required=False, label="PDF сертификата")

    class Meta:
        icon = 'certificate'
        label = "Сертификат"


class CertificatesIndexPage(Page):
    intro = models.TextField(blank=True, verbose_name="Вступительный текст")

    body = StreamField([
        ('certificate', CertificateBlock()),
    ], use_json_field=True, collapsed=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('body'),
    ]

    subpage_types = []
    parent_page_types = ['home.HomePage']

    def get_context(self, request):
        context = super().get_context(request)
        certificates = [block.value for block in self.body if block.block_type == 'certificate']
        
        # Сортировка по дате (новые сверху)
        certificates.sort(key=lambda x: x['issue_date'], reverse=True)

        # Пагинация
        from django.core.paginator import Paginator
        paginator = Paginator(certificates, 12)
        page = request.GET.get('page')
        context['certificates'] = paginator.get_page(page)

        return context
    class Meta:
        verbose_name = "Страница 'Сертификаты'"
        verbose_name_plural = "Страница 'Сертификатов' "
