# board/templatetags/board_extras.py
from django import template

register = template.Library()  # 필수

@register.filter
def any_has_image(files):
    return any(f.image for f in files)

@register.filter
def any_has_file(files):
    return any(f.file for f in files)

# board_extras.py
@register.filter
def parse_tag_name(tag_value):
    if isinstance(tag_value, str) and tag_value.startswith('['):
        try:
            import json
            parsed = json.loads(tag_value)
            return parsed[0].get('value', tag_value)
        except:
            return tag_value
    return tag_value

