from .models import AdminNotification


def create_admin_notification(title, message, url=None) -> AdminNotification:
    """Создает новое уведомление в базе данных."""
    return AdminNotification.objects.create(title=title, message=message, url=url)
