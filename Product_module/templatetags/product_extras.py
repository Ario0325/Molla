from django import template
import locale

register = template.Library()

@register.filter(name='price_format')
def price_format(value):
    try:
        return "{:,}".format(int(value)) + ' تومان'
    except:
        return value

@register.filter(name='discount_label')
def discount_label(discount_percent):
    try:
        return f"{int(discount_percent)}% تخفیف"
    except:
        return ""
