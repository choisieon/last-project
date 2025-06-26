# board/templatetags/board_extras.py
from django import template

register = template.Library()  # 필수

@register.filter
def any_has_image(files):
    return any(f.image for f in files)

@register.filter
def any_has_file(files):
    return any(f.file for f in files)
