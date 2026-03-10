import logging

from config.settings.dev import EMAIL_HOST_USER
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

logger = logging.getLogger(__name__)


# Получить email пользователей в определенных группах
def get_emails_by_group_names(group_names, user) -> list:
    users = user.objects.filter(groups__name__in=group_names).distinct()
    return [user_.email for user_ in users if user_.email]


def send_admin_notification(notification_instance) -> None:
    try:
        user = get_user_model()
        admins = user.objects.filter(is_superuser=True)
        group_names = list(Group.objects.values_list("name", flat=True))
        context = {
            "title": notification_instance.title,
            "message": notification_instance.message,
            "url": notification_instance.url,
            "created_at": notification_instance.created_at,
            "notification": notification_instance,
        }
        admin_emails = [user_.email for user_ in admins if user_.email] # type: ignore  # noqa: E261, PGH003
        editor_moderator_emails = get_emails_by_group_names(group_names, user)

        all_emails = admin_emails + editor_moderator_emails

        if not all_emails:
            logger.warning("Нет ни одного email администратора для отправки уведомлений")
            return

        subject = f"Уведомление: {notification_instance.title}"

        html_message = render_to_string("emails/admin_notification.html", context)
        text_message = strip_tags(html_message)

        email = EmailMultiAlternatives(
            subject=subject,
            body=text_message,
            from_email=EMAIL_HOST_USER,
            to=all_emails,
        )
        email.attach_alternative(html_message, "text/html")

        result = email.send(fail_silently=False)
        logger.info("Admin notification email sent. Result: %s", result)

    except Exception as e:  # noqa: BLE001
        logger.error(f"Failed to send admin notification email: {e!s}")  # noqa: G004, TRY400
