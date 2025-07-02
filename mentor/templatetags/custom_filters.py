from django import template
register = template.Library()

@register.filter
def normalize_linebreaks(value):
    return value.replace('\r\n', '\n').replace('\r', '\n')