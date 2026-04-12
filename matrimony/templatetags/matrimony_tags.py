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
    return code.replace('லக்', '<strong style="color:#8b1a1a;font-weight:700;text-decoration:underline;">ல</strong>க்')

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

    # Compound thousand forms (1-99 * 1000)
    th_prefix = ['', 'ஆயிரம்', 'இரண்டாயிரம்', 'மூவாயிரம்', 'நான்காயிரம்',
                 'ஐயாயிரம்', 'ஆறாயிரம்', 'ஏழாயிரம்', 'எட்டாயிரம்', 'ஒன்பதாயிரம்',
                 'பத்தாயிரம்', 'பதினோராயிரம்', 'பன்னிரண்டாயிரம்', 'பதிமூவாயிரம்',
                 'பதினான்காயிரம்', 'பதினைந்தாயிரம்', 'பதினாறாயிரம்', 'பதினேழாயிரம்',
                 'பதினெட்டாயிரம்', 'பத்தொன்பதாயிரம்', 'இருபதாயிரம்', 'இருபத்தோராயிரம்',
                 'இருபத்திரண்டாயிரம்', 'இருபத்துமூவாயிரம்', 'இருபத்துநான்காயிரம்',
                 'இருபத்தைந்தாயிரம்', 'இருபத்தாறாயிரம்', 'இருபத்தேழாயிரம்',
                 'இருபத்தெட்டாயிரம்', 'இருபத்தொன்பதாயிரம்', 'முப்பதாயிரம்',
                 'முப்பத்தோராயிரம்', 'முப்பத்திரண்டாயிரம்', 'முப்பத்துமூவாயிரம்',
                 'முப்பத்துநான்காயிரம்', 'முப்பத்தைந்தாயிரம்', 'முப்பத்தாறாயிரம்',
                 'முப்பத்தேழாயிரம்', 'முப்பத்தெட்டாயிரம்', 'முப்பத்தொன்பதாயிரம்',
                 'நாற்பதாயிரம்', 'நாற்பத்தோராயிரம்', 'நாற்பத்திரண்டாயிரம்',
                 'நாற்பத்துமூவாயிரம்', 'நாற்பத்துநான்காயிரம்', 'நாற்பத்தைந்தாயிரம்',
                 'நாற்பத்தாறாயிரம்', 'நாற்பத்தேழாயிரம்', 'நாற்பத்தெட்டாயிரம்',
                 'நாற்பத்தொன்பதாயிரம்', 'ஐம்பதாயிரம்', 'ஐம்பத்தோராயிரம்',
                 'ஐம்பத்திரண்டாயிரம்', 'ஐம்பத்துமூவாயிரம்', 'ஐம்பத்துநான்காயிரம்',
                 'ஐம்பத்தைந்தாயிரம்', 'ஐம்பத்தாறாயிரம்', 'ஐம்பத்தேழாயிரம்',
                 'ஐம்பத்தெட்டாயிரம்', 'ஐம்பத்தொன்பதாயிரம்', 'அறுபதாயிரம்',
                 'அறுபத்தோராயிரம்', 'அறுபத்திரண்டாயிரம்', 'அறுபத்துமூவாயிரம்',
                 'அறுபத்துநான்காயிரம்', 'அறுபத்தைந்தாயிரம்', 'அறுபத்தாறாயிரம்',
                 'அறுபத்தேழாயிரம்', 'அறுபத்தெட்டாயிரம்', 'அறுபத்தொன்பதாயிரம்',
                 'எழுபதாயிரம்', 'எழுபத்தோராயிரம்', 'எழுபத்திரண்டாயிரம்',
                 'எழுபத்துமூவாயிரம்', 'எழுபத்துநான்காயிரம்', 'எழுபத்தைந்தாயிரம்',
                 'எழுபத்தாறாயிரம்', 'எழுபத்தேழாயிரம்', 'எழுபத்தெட்டாயிரம்',
                 'எழுபத்தொன்பதாயிரம்', 'எண்பதாயிரம்', 'எண்பத்தோராயிரம்',
                 'எண்பத்திரண்டாயிரம்', 'எண்பத்துமூவாயிரம்', 'எண்பத்துநான்காயிரம்',
                 'எண்பத்தைந்தாயிரம்', 'எண்பத்தாறாயிரம்', 'எண்பத்தேழாயிரம்',
                 'எண்பத்தெட்டாயிரம்', 'எண்பத்தொன்பதாயிரம்', 'தொண்ணூறாயிரம்',
                 'தொண்ணூத்தோராயிரம்', 'தொண்ணூத்திரண்டாயிரம்', 'தொண்ணூத்துமூவாயிரம்',
                 'தொண்ணூத்துநான்காயிரம்', 'தொண்ணூத்தைந்தாயிரம்', 'தொண்ணூத்தாறாயிரம்',
                 'தொண்ணூத்தேழாயிரம்', 'தொண்ணூத்தெட்டாயிரம்', 'தொண்ணூத்தொன்பதாயிரம்']

    def below_hundred(num):
        if num < 20: return ones[num]
        elif num % 10 == 0: return tens[num // 10]
        return tens[num // 10] + ' ' + ones[num % 10]

    def below_thousand(num):
        if num < 100: return below_hundred(num)
        h = num // 100; r = num % 100
        res = ones[h] + ' நூறு'
        if r: res += ' ' + below_hundred(r)
        return res

    result = ''
    orig_n = n

    if n >= 10000000:  # crore
        cr = n // 10000000
        word = below_thousand(cr) + ' கோடி'
        if cr == 1: word = 'ஒரு கோடி'
        result += word + ' '
        n %= 10000000

    if n >= 100000:  # lakh
        lk = n // 100000
        word = below_thousand(lk) + ' லட்சம்'
        if lk == 1:
            word = 'ஒரு லட்சம்' if n % 100000 == 0 else 'ஒரு லட்சத்து'
        result += word + ' '
        n %= 100000

    if n >= 1000:  # thousands (1-99)
        th = n // 1000
        if th <= 99:
            result += th_prefix[th]
        else:
            result += below_thousand(th) + ' ஆயிரம்'
        n %= 1000
        if n > 0:
            result += ' '

    if n > 0:
        result += below_thousand(n)

    return result.strip() + ' ரூபாய்'


@register.filter
def smart_salary(value):
    """
    Format salary smartly:
    - None/0        → empty string
    - < 1,00,000    → ₹XX,XXX (comma separated)
    - >= 1,00,000   → ₹X lakh / ₹X.XX lakh
    """
    if not value:
        return ''
    try:
        amount = float(value)
    except (TypeError, ValueError):
        return ''
    if amount <= 0:
        return ''
    if amount < 100000:
        # Format with Indian comma style
        val = int(amount)
        s = str(val)
        if len(s) > 3:
            last3 = s[-3:]
            rest = s[:-3]
            parts = []
            while len(rest) > 2:
                parts.append(rest[-2:])
                rest = rest[:-2]
            if rest:
                parts.append(rest)
            parts.reverse()
            s = ','.join(parts) + ',' + last3
        return f'₹{s}'
    else:
        lakhs = amount / 100000
        if lakhs == int(lakhs):
            return f'₹{int(lakhs)} lakh'
        else:
            # Round to 2 decimal places, strip trailing zeros
            formatted = f'{lakhs:.2f}'.rstrip('0').rstrip('.')
            return f'₹{formatted} lakh'


@register.simple_tag
def display_salary(candidate):
    """
    Show monthly salary if present, else annual income.
    Uses smart_salary format.
    Label changes accordingly.
    Returns tuple (label, value) — use as {% display_salary candidate as label value %}
    Actually returns formatted HTML string.
    """
    from django.utils.safestring import mark_safe
    monthly = candidate.monthly_salary
    annual  = candidate.annual_income
    if monthly:
        label = 'வருமானம்'
        val   = smart_salary(monthly) + ' per month'
    elif annual:
        label = 'வருமானம்'
        val   = smart_salary(annual) + ' per annum'
    else:
        from .models import MaleCandidate
        if isinstance(candidate, MaleCandidate):
            label = 'வருமானம்'
            val   = 'நேரில்'
        else:
            return mark_safe('')
    return mark_safe(f'<tr><td>{label}</td><td class="colon">:</td><td style="white-space:nowrap;">{val}</td></tr>')
