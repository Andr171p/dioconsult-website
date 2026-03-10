# forms.py
from typing import ClassVar

import re

from django import forms
from django.core.validators import validate_email
from utils import check_spam

from .models import FeedbackMessage


class FeedbackForm(forms.ModelForm):
    csrftoken = forms.CharField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = FeedbackMessage
        fields: ClassVar[list[str]] = [
            "email",
            "message",
        ]
        widgets: ClassVar[dict] = {
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email"}),
            "message": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "Сообщение", "rows": 4}
            ),
        }

    def clean_email(self):
        """Валидация email"""
        email = self.cleaned_data.get("email")

        if email:
            # Базовая проверка формата
            try:
                validate_email(email)
            except forms.ValidationError:
                raise forms.ValidationError("Введите корректный email адрес") from None
        return email

   

    def clean_csrftoken(self) -> str | None:
        csrftoken = self.cleaned_data.get("csrftoken")
        if csrftoken:
            check_spam(csrftoken)
        return csrftoken
