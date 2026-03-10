from typing import ClassVar

from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet

from .models import AdminNotification


class AdminNotificationViewSet(SnippetViewSet):
    model = AdminNotification
    menu_label = "Уведомления"
    menu_icon = "warning"
    menu_order = 300
    add_to_settings_menu = False
    list_display = ("title", "created_at", "is_read")
    list_filter = ("title", "is_read", "created_at")
    search_fields = "message"
    add_to_admin_menu = True

    panels: ClassVar[list[FieldPanel]] = [
        MultiFieldPanel([
            FieldPanel("title", read_only=True),
            FieldPanel("message", read_only=True),
            FieldPanel("url", read_only=True),
        ]),
        FieldPanel("is_read"),
    ]


register_snippet(AdminNotificationViewSet)
