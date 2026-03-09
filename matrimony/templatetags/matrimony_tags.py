from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def get_planet_name(candidate, field_name):
    """Get planet code for a jathagam house field e.g. rasi_h1"""
    try:
        planet = getattr(candidate, field_name, None)
        return planet.code if planet else ''
    except Exception:
        return ''

@register.filter
def get_planet_id(candidate, field_name):
    """Get planet FK id for selected state in dropdown"""
    try:
        planet = getattr(candidate, field_name, None)
        return planet.pk if planet else ''
    except Exception:
        return ''

@register.simple_tag
def planet_select(name, candidate, planets):
    """Render a planet select dropdown"""
    current_id = ''
    if candidate:
        try:
            planet = getattr(candidate, name, None)
            if planet:
                current_id = planet.pk
        except Exception:
            pass

    options = '<option value="">-</option>'
    for p in planets:
        selected = 'selected' if p.pk == current_id else ''
        options += f'<option value="{p.pk}" {selected}>{p.code}</option>'
    return mark_safe(f'<select name="{name}" class="jathagam-select">{options}</select>')

@register.filter
def format_12hr(time_val):
    """Convert time to 12hr AM/PM format"""
    if not time_val:
        return ''
    try:
        hour = time_val.hour
        minute = time_val.minute
        am_pm = 'AM' if hour < 12 else 'PM'
        hour12 = hour % 12 or 12
        return f"{hour12:02d}:{minute:02d} {am_pm}"
    except Exception:
        return str(time_val)
