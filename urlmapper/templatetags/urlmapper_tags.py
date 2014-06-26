from django import template

from ..helpers import get_mapped_url, check_mapped_url

register = template.Library()


@register.simple_tag(takes_context=True)
def mapped_url(context, key):
    return get_mapped_url(key, context.get('request'))


@register.filter
def is_mapped_url(key):
    return check_mapped_url(key)
