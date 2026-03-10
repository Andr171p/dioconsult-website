from chat import views as chat_views
from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve
from feedback import views as feedback_views
from search import views as search_views
from vacancy import views as vacancies_views
from vacancy.wagtail_hooks import download_resume
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("search/", search_views.search, name="search"),
    path("api/", include("vacancy.urls")),
    path("chat/", chat_views.chat, name="chat"),
    path("documents/add/", chat_views.add_document_, name="add document"),
    path("documents/upload/", chat_views.upload_document_, name="upload document"),
    path("documents/delete/", chat_views.delete_document_, name="delete document"),
    path("feedback/", feedback_views.feedback_view, name="feedback"),
    path("vacancy/", vacancies_views.vacancy_view, name="vacancy"),
    path(
        "vacancy/resume/download/<int:vacancy_id>/",
        download_resume,
        name="download_resume",
    ),
    path("", include("wagtail.urls")),
]
urlpatterns += [
    re_path(
        r"^media/(?P<path>.*)$",
        serve,
        {
            "document_root": settings.MEDIA_ROOT,
            "show_indexes": False,
        },
    ),
]
