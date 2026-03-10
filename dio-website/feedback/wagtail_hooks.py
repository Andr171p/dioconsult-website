from typing import ClassVar

from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet

from .models import FeedbackMessage


class FeedbackMessageViewSet(SnippetViewSet):
    model = FeedbackMessage
    menu_label = "Обратная связь"
    menu_icon = "comment"
    menu_order = 300
    add_to_settings_menu = False
    list_display = ("email", "created_at", "is_processed")
    list_filter = ("created_at", "is_processed")
    search_fields = ("email", "message")
    add_to_admin_menu = True

    panels: ClassVar[list[FieldPanel]] = [
        MultiFieldPanel([
            FieldPanel("email", read_only=True),
            FieldPanel("message", read_only=True),
        ]),
        FieldPanel("is_processed"),
    ]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if qs is None:
            qs = FeedbackMessage.objects.all()

        return qs.order_by("-created_at")

    def has_add_permission(self, request):  # noqa: ARG002, PLR6301
        return False


register_snippet(FeedbackMessageViewSet)
