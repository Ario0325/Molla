from django import template
import locale

register = template.Library()

@register.filter(name='price_format')
def price_format(value):
    try:
        return "{:,}".format(int(value)) + ' تومان'
    except:
        return value
