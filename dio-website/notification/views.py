from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect

from .models import AdminNotification


@login_required
def toggle_notification_read(request, notification_id):
    notification = get_object_or_404(AdminNotification, id=notification_id)
    notification.is_read = not notification.is_read
    notification.save()
    return redirect(request.META.get("HTTP_REFERER", "wagtailadmin_home"))
