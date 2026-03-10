from django import template

register = template.Library()

@register.filter
def split(value, delimiter="\n"):
    """Разделяет строку на список по указанному разделителю."""
    if isinstance(value, str):
        return value.split(delimiter)
    return value
