from django import template

from django.utils.text import slugify as original_slugify

register = template.Library()


@register.filter(name='slugify')
def slugify(value):
    return original_slugify(value, allow_unicode=True)
