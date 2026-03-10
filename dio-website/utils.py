import os  # noqa: INP001

import pytz
from django import forms
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.utils import timezone


def get_tumen_time():
    yekaterinburg_tz = pytz.timezone("Asia/Yekaterinburg")

    now = timezone.now()

    return now.astimezone(yekaterinburg_tz)


def check_spam(csrftoken: str) -> None:
    count = cache.get(csrftoken) or 0
    if count >= 3:  # noqa: PLR2004
        raise forms.ValidationError("Вы отправили слишком много заявок. Попробуйте позже.")
    cache.set(csrftoken, count + 1, 60 * 60)


def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = [".pdf", ".doc", ".docx", ".txt"]
    if ext.lower() not in valid_extensions:
        raise ValidationError("Поддерживаются только файлы PDF, DOC, DOCX и TXT")
