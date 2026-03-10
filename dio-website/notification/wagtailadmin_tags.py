from django import template

from .models import AdminNotification

register = template.Library()


@register.simple_tag(takes_context=True)
def get_unread_notifications(context) -> AdminNotification:  # noqa: ARG001
    return AdminNotification.objects.filter(is_read=False)
