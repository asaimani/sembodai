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


def _format_planet_code(code):
    """Replace லக் with HTML underlined version."""
    return code.replace('லக்', '<u>ல</u>க்')

def _format_planet_codes(codes_str):
    """Apply formatting to comma-separated planet codes string."""
    if not codes_str:
        return ''
    parts = [_format_planet_code(c.strip()) for c in codes_str.split(',')]
    return ', '.join(parts)

@register.simple_tag
def house_display(jathagam_map, chart_key, house_number):
    """
    Return comma-separated planet codes for a house in view/print mode.
    chart_key : 'R' or 'N'
    """
    from django.utils.safestring import mark_safe
    if not jathagam_map:
        return ''
    raw = jathagam_map.get(chart_key, {}).get(house_number, '')
    return mark_safe(_format_planet_codes(raw))


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


@register.filter
def amount_in_tamil_words(value):
    """Convert number to Tamil words. e.g. 10000 → பத்தாயிரம் ரூபாய்"""
    try:
        n = int(value)
    except (ValueError, TypeError):
        return value

    if n == 0:
        return 'பூஜ்யம் ரூபாய்'

    ones = ['', 'ஒன்று', 'இரண்டு', 'மூன்று', 'நான்கு', 'ஐந்து',
            'ஆறு', 'ஏழு', 'எட்டு', 'ஒன்பது', 'பத்து', 'பதினொன்று',
            'பன்னிரண்டு', 'பதிமூன்று', 'பதினான்கு', 'பதினைந்து',
            'பதினாறு', 'பதினேழு', 'பதினெட்டு', 'பத்தொன்பது']

    tens = ['', '', 'இருபது', 'முப்பது', 'நாற்பது', 'ஐம்பது',
            'அறுபது', 'எழுபது', 'எண்பது', 'தொண்ணூறு']

    def below_hundred(num):
        if num < 20:
            return ones[num]
        elif num % 10 == 0:
            return tens[num // 10]
        else:
            return tens[num // 10] + ' ' + ones[num % 10]

    def below_thousand(num):
        if num < 100:
            return below_hundred(num)
        else:
            h = num // 100
            r = num % 100
            result = ones[h] + ' நூறு'
            if r:
                result += ' ' + below_hundred(r)
            return result

    result = ''
    if n >= 10000000:  # crore
        cr = n // 10000000
        result += below_thousand(cr) + ' கோடி '
        n %= 10000000
    if n >= 100000:  # lakh
        lk = n // 100000
        result += below_thousand(lk) + ' லட்சம் '
        n %= 100000
    if n >= 1000:  # thousand
        th = n // 1000
        result += below_thousand(th) + ' ஆயிரம் '
        n %= 1000
    if n > 0:
        result += below_thousand(n)

    return result.strip() + ' ரூபாய்'
