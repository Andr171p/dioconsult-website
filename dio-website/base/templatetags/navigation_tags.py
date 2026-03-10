from django import template
from wagtail.models import Page, Site

register = template.Library()


@register.simple_tag(takes_context=True)
def get_site_root(context: dict[str, object]) -> Page:
    """Получает корневую страницу сайта"""
    return Site.find_for_request(context["request"]).root_page
