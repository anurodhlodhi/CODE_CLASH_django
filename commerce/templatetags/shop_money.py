from django import template

register = template.Library()


@register.filter
def rupees(paise):
    return f"₹{int(paise) / 100:,.2f}"
