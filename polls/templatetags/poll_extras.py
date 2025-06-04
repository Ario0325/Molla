from django import template
from jalali_date import datetime2jalali, date2jalali

register = template.Library()

@register.filter(name='jalali_date')
def show_jalali_date_value(value):
    return date2jalali(value)

@register.filter(name='jalali_time')
def show_jalali_time_value(value):
    return datetime2jalali(value).time()

@register.filter(name='three_digits_currency')
def three_digits_currency(value: int):
    return "{:,}".format(value) + " تومان"