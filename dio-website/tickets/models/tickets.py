from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class Tag(models.Model):
    """Теги - метки (ключевые слова), которые можно присваивать тикетам для дополнительной,
    неструктурированной классификации
    """

    name = models.CharField(max_length=50, unique=True)
    color = models.CharField(max_length=7, default="#3498db", verbose_name="HEX код цвета")

    def __str__(self) -> str:
        return self.name


class Ticket(models.Model):
    """Модель тикета"""

    STATUS_CHOICES = [
        ("new", "Новый"),  # только что создан, ещё не обработан
        ("open", "Открыт"),  # принят в работу
        ("in_progress", "В работе"),  # активная работа
        ("waiting", "Ожидание"),  # ждём ответа клиента или внешних действий
        ("resolved", "Решён"),   # проблема решена, ожидает подтверждения клиента
        ("closed", "Закрыт"),  # окончательно закрыт (клиент подтвердил или автоматически)
        ("reopened", "Переоткрыт"),  # клиент не согласен с решением
    ]
    PRIORITY_CHOICES = [
        ("low", "Низкий"),
        ("medium", "Средний"),
        ("high", "Высокий"),
        ("critical", "Критический"),
    ]

    company = models.ForeignKey(
        "Company",
        on_delete=models.CASCADE,
        related_name="tickets",
        verbose_name="Компания",
        null=True,
        blank=True,
    )
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    description = models.TextField(verbose_name="Описание")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="open",
        db_index=True,
        verbose_name="Статус"
    )
    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default="medium",
        verbose_name="Приоритет"
    )
    category = models.ForeignKey(
        "Category",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Категория",
        related_name="tickets"
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="created_tickets",
        verbose_name="Автор"
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_tickets",
        verbose_name="Исполнитель",
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name="tickets")
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="Создан")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлён")
    closed_at = models.DateTimeField(null=True, blank=True, verbose_name="Закрыт")
    is_archived = models.BooleanField(default=False, verbose_name="В архиве")

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status", "priority"]),
            models.Index(fields=["created_by", "status"]),
        ]
        verbose_name = "Тикет"
        verbose_name_plural = "Тикеты"
        permissions = [
            ("view_company_tickets", "Может просматривать все тикеты своей компании"),
        ]

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs) -> None:
        if not self.pk and not self.company and self.created_by:
            first_company = self.created_by.companies.first()
            if first_company:
                self.company = first_company
        super().save(*args, **kwargs)


class Category(models.Model):
    """Справочник категорий (тематик) тикетов"""

    name = models.CharField(max_length=100, unique=True, verbose_name="Название")
    description = models.TextField(blank=True, verbose_name="Описание")
    default_assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="default_categories",
        verbose_name="Ответственный по умолчанию"
    )
    order = models.PositiveSmallIntegerField(default=0, verbose_name="Порядок")

    class Meta:
        ordering = ["order", "name"]
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self) -> str:
        return self.name


class Comment(models.Model):
    """Комментарий к тикету"""

    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Тикет"
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Автор"
    )
    text = models.TextField(verbose_name="Текст")
    is_private = models.BooleanField(
        default=False,
        verbose_name="Внутренний комментарий",
        help_text="Виден только агентам поддержки"
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["created_at"]
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"


class Attachment(models.Model):
    """Вложение, могут быть привязаны как к тикету на прямую, так и конкретному комментарию"""

    file = models.FileField(
        upload_to="tickets/attachments/%Y/%m/%d/",
        verbose_name="Файл"
    )
    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name="attachments",
        null=True, blank=True
    )
    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        related_name="attachments",
        null=True, blank=True
    )
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Загрузил"
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Вложение"
        verbose_name_plural = "Вложения"

    def clean(self) -> None:
        if (self.ticket is None) == (self.comment is None):
            raise ValidationError(
                "Вложение должно быть привязано либо к тикету, либо к комментарию!"
            )
