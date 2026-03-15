from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def planet_multiselect(prefix, house_number, jathagam_map, planets):
    """
    Render a multi-select dropdown for one house in the jathagam grid.
    prefix       : 'rasi' or 'navamsam'
    house_number : 1–12
    jathagam_map : dict from candidate.get_jathagam_map()
    planets      : queryset of all Planet objects

    Field name uses [] suffix so POST delivers a list:
      rasi_h1[]  navamsam_h6[]  etc.
    Up to 9 planets can be selected (enforced in JS).
    """
    chart_key = 'R' if prefix == 'rasi' else 'N'
    current_text = ''
    if jathagam_map:
        current_text = jathagam_map.get(chart_key, {}).get(house_number, '')

    selected_codes = set(c.strip() for c in current_text.split(',') if c.strip())
    code_to_pk = {p.code: p.pk for p in planets}
    selected_pks = {code_to_pk[c] for c in selected_codes if c in code_to_pk}

    field_name = f'{prefix}_h{house_number}[]'
    options = ''
    for p in planets:
        sel = 'selected' if p.pk in selected_pks else ''
        options += f'<option value="{p.pk}" {sel}>{p.code}</option>'

    html = (
        f'<select name="{field_name}" '
        f'class="jathagam-select" '
        f'multiple size="3" data-max="9">'
        f'{options}'
        f'</select>'
    )
    return mark_safe(html)


@register.simple_tag
def house_display(jathagam_map, chart_key, house_number):
    """
    Return comma-separated planet codes for a house in view/print mode.
    chart_key : 'R' or 'N'
    """
    if not jathagam_map:
        return ''
    return jathagam_map.get(chart_key, {}).get(house_number, '')


@register.filter
def format_12hr(time_val):
    if not time_val:
        return ''
    try:
        hour, minute = time_val.hour, time_val.minute
        am_pm = 'AM' if hour < 12 else 'PM'
        return f"{hour % 12 or 12:02d}:{minute:02d} {am_pm}"
    except Exception:
        return str(time_val)
