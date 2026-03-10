from django.db import models
from django.contrib.auth.models import AbstractUser

class Company(models.Model):
    name = models.CharField("Название компании", max_length=255)
    slug = models.SlugField("Слаг (URL)", unique=True)
    email = models.EmailField("Email")
    created_at = models.DateTimeField("Дата регистрации", auto_now_add=True)
    assigned_manager = models.ForeignKey(
        'CustomUser', on_delete=models.SET_NULL, null=True, blank=True, 
        related_name='managed_companies', verbose_name="Менеджер ДИО"
    )

    class Meta:
        verbose_name = "Компания"
        verbose_name_plural = "Компании"

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, null=True, blank=True, 
        related_name='employees', verbose_name="Компания"
    )
    is_company_boss = models.BooleanField("Босс компании", default=False)
    is_internal = models.BooleanField("Сотрудник ДИО", default=False)
    phone = models.CharField("Телефон", max_length=20, blank=True)
    receive_notifications = models.BooleanField("Уведомления", default=True)

    def save(self, *args, **kwargs):
        # Автоматически даем доступ в админку Боссам и ДИО
        if self.is_company_boss or self.is_internal or self.is_superuser:
            self.is_staff = True
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

class Ticket(models.Model):
    STATUS_CHOICES = (
        ('new', 'Новый'),
        ('in_progress', 'В работе'),
        ('done', 'Выполнен'),
        ('closed', 'Закрыт'),
    )
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name="Компания")
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='mytickets', verbose_name="Автор")
    assigned_to = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, blank=True, 
        related_name='worktickets', verbose_name="Исполнитель"
    )
    title = models.CharField("Тема", max_length=255)
    description = models.TextField("Описание")
    status = models.CharField("Статус", max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Тикет"
        verbose_name_plural = "Тикеты"

    def __str__(self):
        return f"#{self.id} {self.title}"

class TicketMessage(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='messages', verbose_name="Тикет")
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Автор")
    message = models.TextField("Сообщение")
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField("Прочитано", default=False)

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"