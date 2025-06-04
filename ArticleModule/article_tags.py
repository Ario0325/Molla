from django import template

register = template.Library()

@register.filter
def reading_time_display(minutes):
    if minutes < 1:
        return "کمتر از یک دقیقه"
    return f"{minutes} دقیقه"
