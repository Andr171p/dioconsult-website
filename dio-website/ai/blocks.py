import re

from django.core.exceptions import ValidationError
from wagtail.blocks import CharBlock, ListBlock, StructBlock


class KeyValueItemBlock(StructBlock):
    key = CharBlock(required=True, label="Название")
    value = CharBlock(required=True, label="Содержание")

    def clean(self, value) -> super:
        """Проверка, что ключ содержит только английские символы."""
        cleaned_data = super().clean(value)
        key_value = cleaned_data["key"]

        if not re.match(r"^[a-zA-Z0-9_-]+$", key_value):
            raise ValidationError(
                "Ключ должен содержать только английские буквы, цифры и символы '-' или '_'"
            )
        return cleaned_data

    class Meta:
        icon = "tag"
        template = "blocks/key_value_item.html"


class MetadataBlock(ListBlock):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(KeyValueItemBlock(), *args, **kwargs)

    class Meta:
        icon = "list-ul"
        label = "Метаданные"
        template = "blocks/metadata.html"
