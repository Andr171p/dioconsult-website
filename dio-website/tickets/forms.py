from typing import Any

from django import forms

from .models import Invitation


class SetPasswordForm(forms.Form):
    """Форма для установки пароля"""

    password = forms.CharField(widget=forms.PasswordInput, min_length=8, label="Пароль")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Подтверждение")

    def clean(self) -> dict[str, Any]:
        """Проверка на равенство введенных паролей"""

        cleaned_data = super().clean()
        if cleaned_data.get("password") != self.cleaned_data.get("confirm_password"):
            raise forms.ValidationError("Введенные пароли не совпадают!", code="invalid")
        return cleaned_data


class InvitationInlineForm(forms.ModelForm):
    class Meta:
        model = Invitation
        fields = [
            "email",
            "default_counterparty_role",
            "expires_at",
            "is_used",
            "created_by",
        ]

    def clean_email(self) -> str:
        email = self.cleaned_data["email"].lower().strip()
        if Invitation.objects.filter(
            email=email, counterparty=self.instance.counterparty, is_used=False
        ).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Ha этот email уже отправлено приглашение!")
        return email
