from django import template

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
    return f'<select name="{name}" class="jathagam-select">{options}</select>'
