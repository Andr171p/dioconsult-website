from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm
from django.utils.html import format_html
from .models import Company, CustomUser, Ticket, TicketMessage

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'company', 'is_company_boss', 'phone')

class BossAccessMixin:
    def has_module_permission(self, request):
        return request.user.is_staff

    def has_view_permission(self, request, obj=None):
        return request.user.is_staff

    def has_add_permission(self, request):
        return request.user.is_staff

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser or request.user.is_internal:
            return True
        if obj and hasattr(obj, 'company'):
            return obj.company == request.user.company
        if obj and isinstance(obj, CustomUser):
            return obj.company == request.user.company
        return request.user.is_company_boss

    def has_delete_permission(self, request, obj=None):
        return self.has_change_permission(request, obj)

@admin.register(CustomUser)
class CustomUserAdmin(BossAccessMixin, UserAdmin):
    add_form = CustomUserCreationForm 
    list_display = ('username', 'company', 'is_company_boss', 'is_internal', 'is_staff')
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Персональные данные', {'fields': ('first_name', 'last_name', 'email', 'phone')}),
        ('Служебная информация', {'fields': ('company', 'is_company_boss', 'is_internal', 'receive_notifications')}),
        ('Права', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password', 'first_name', 'last_name', 'email', 'company', 'is_company_boss', 'phone'),
        }),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser or request.user.is_internal:
            return qs
        if request.user.is_company_boss:
            return qs.filter(company=request.user.company)
        return qs.filter(id=request.user.id)

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser and not request.user.is_internal and request.user.is_company_boss:
            obj.company = request.user.company
        super().save_model(request, obj, form, change)

class MessageInline(admin.TabularInline):
    model = TicketMessage
    extra = 1
    fields = ('author', 'message', 'created_at')
    readonly_fields = ('created_at',)

@admin.register(Ticket)
class TicketAdmin(BossAccessMixin, admin.ModelAdmin):
    list_display = ('id', 'title', 'company', 'created_by', 'assigned_to', 'colored_status')
    list_filter = ('status',)
    inlines = [MessageInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser or request.user.is_internal:
            return qs
        if request.user.is_company_boss:
            return qs.filter(company=request.user.company)
        return qs.filter(created_by=request.user)

    def colored_status(self, obj):
        colors = {'new': '#ff4d4d', 'in_progress': '#3399ff', 'done': '#2eb82e', 'closed': '#999999'}
        return format_html('<b style="color: {};">{}</b>', colors.get(obj.status), obj.get_status_display())
    colored_status.short_description = "Статус"

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
            if not request.user.is_internal:
                obj.company = request.user.company
        super().save_model(request, obj, form, change)

@admin.register(Company)
class CompanyAdmin(BossAccessMixin, admin.ModelAdmin):
    list_display = ('name', 'email', 'assigned_manager')
    prepopulated_fields = {'slug': ('name',)}

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser or request.user.is_internal:
            return qs
        return qs.filter(id=request.user.company_id)

@admin.register(TicketMessage)
class MessageAdmin(BossAccessMixin, admin.ModelAdmin):
    list_display = ('ticket', 'author', 'created_at')
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser or request.user.is_internal:
            return qs
        return qs.filter(ticket__company=request.user.company)