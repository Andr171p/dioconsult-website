from typing import Any

from django import forms


class SetPasswordForm(forms.Form):
    """Форма для установки пароля"""

    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Подтверждение")

    def clean(self) -> dict[str, Any]:
        """Проверка на равенство введенных паролей"""

        cleaned_data = super().clean()
        if cleaned_data.get("password") != self.cleaned_data.get("confirm_password"):
            raise forms.ValidationError("Введенные пароли не совпадают!", code="invalid")
        return cleaned_data
