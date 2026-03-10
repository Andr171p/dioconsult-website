# vacancy/wagtail_hooks.py
from typing import ClassVar
import os
from django.db.models import QuerySet
from django.http import FileResponse, HttpResponse
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from wagtail import hooks
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.admin.ui.components import Component
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet
from .models import Vacancy


class VacancyViewSet(SnippetViewSet):
    model = Vacancy
    menu_label = "Вакансии"
    menu_icon = "table"
    menu_order = 300
    add_to_settings_menu = False
    list_display = ("title", "created_at", "is_processed")
    list_filter = ("created_at", "is_processed")
    search_fields = ("title", "name", "phone")
    add_to_admin_menu = True

    panels: ClassVar[list] = [
        MultiFieldPanel(
            [
                FieldPanel("title", read_only=True),
                FieldPanel("name", read_only=True),
                FieldPanel("phone", read_only=True),
                FieldPanel("created_at", read_only=True),
                FieldPanel("resume_link", read_only=True),
            ],
            heading="Информация о кандидате",
        ),
        FieldPanel("is_processed"),
    ]

    def get_queryset(self, request) -> QuerySet:
        qs = super().get_queryset(request)
        if qs is None:
            qs = Vacancy.objects.all()
        return qs.order_by("-created_at")

    def has_add_permission(self, request) -> bool:
        return False


def download_resume(request, vacancy_id):
    try:
        vacancy = Vacancy.objects.get(id=vacancy_id)
        if not vacancy.resume:
            return HttpResponse("Файл не найден", status=404)

        file_path = vacancy.resume.path
        if not os.path.exists(file_path):
            return HttpResponse("Файл не найден на сервере", status=404)

        file = open(file_path, "rb")
        response = FileResponse(file, content_type="application/octet-stream")
        response["Content-Disposition"] = (
            f'attachment; filename="{os.path.basename(vacancy.resume.name) or "resume"}"'
        )
        response["Content-Length"] = os.path.getsize(file_path)
        return response
    except Vacancy.DoesNotExist:
        return HttpResponse("Вакансия не найдена", status=404)
    except (ValueError, OSError):
        return HttpResponse("Ошибка при загрузке файла", status=500)


register_snippet(VacancyViewSet)
# vacancy/wagtail_hooks.py — 100% Wagtail style
from django.utils.safestring import mark_safe
from wagtail import hooks
from .models import Vacancy


@hooks.register('insert_global_admin_css')
def wagtail_vacancy_style():
    return mark_safe("""
    <style>
    /* Бейдж — точно как у Pages, Images, Documents */
    a.vacancy-badge::after {
        content: attr(data-count);
        display: inline-flex;
        align-items: center;
        justify-content: center;
        min-width: 18px;
        height: 18px;
        padding: 0 6px;
        margin-left: 8px;
        background: #3b82f6;
        color: white;
        font-size: 11px;
        font-weight: 600;
        border-radius: 999px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.2);
        position: relative;
        top: -1px;
    }

    /* Уведомление — как wagtail messages */
    #vacancy-message {
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 9999;
        max-width: 400px;
    }
    </style>
    """)


@hooks.register('insert_global_admin_js')
def wagtail_vacancy_behavior():
    return mark_safe("""
    <script>
    let lastCount = parseInt(localStorage.getItem('vacancy_seen') || '0');

    function updateVacancy() {
        fetch('/api/vacancy-unprocessed-count/')
        .then(r => r.json())
        .then(data => {
            const count = data.count || 0;
            const link = document.querySelector('a[href*="/admin/snippets/vacancy/vacancy/"]');
            if (!link) return;

            // Бейдж
            if (count > 0) {
                link.classList.add('vacancy-badge');
                link.setAttribute('data-count', count > 99 ? '99+' : count);
            } else {
                link.classList.remove('vacancy-badge');
                link.removeAttribute('data-count');
            }

            // Уведомление — только при новых
            if (count > lastCount) {
                const newOnes = count - lastCount;
                showMessage(newOnes);
            }

            lastCount = count;
            localStorage.setItem('vacancy_seen', count);
        });
    }

    function showMessage(newCount) {
        // Удаляем старое
        const old = document.querySelector('#vacancy-message > div');
        if (old) old.remove();

        fetch('/api/latest-unprocessed-vacancy/')
        .then(r => r.ok ? r.json() : {id: null})
        .then(latest => {
            const url = latest.id 
                ? `/admin/snippets/vacancy/vacancy/edit/${latest.id}/`
                : '/admin/snippets/vacancy/vacancy/';

            const container = document.getElementById('vacancy-message') || 
                (() => {
                    const div = document.createElement('div');
                    div.id = 'vacancy-message';
                    document.body.appendChild(div);
                    return div;
                })();

            const msg = document.createElement('div');
            msg.className = 'message success';
            msg.innerHTML = `
                <svg class="icon icon-success messages-icon" aria-hidden="true"><use href="#icon-success"></use></svg>
                <span>Поступил${newCount > 1 ? 'о' : ''} <strong>${newCount}</strong> нов${newCount > 1 ? 'ых' : 'ый'} отклик${newCount > 1 ? 'ов' : ''}!</span>
                <a href="${url}" style="margin-left:12px;color:#3b82f6;font-weight:600;">Открыть</a>
            `;
            container.appendChild(msg);

            setTimeout(() => msg.remove(), 8000);
        });
    }

    updateVacancy();
    setInterval(updateVacancy, 8000);
    </script>
    """)
