from django import template

register = template.Library()


@register.filter
def vnd(value):
    try:
        value = int(value)
        return f"{value:,}".replace(",", ".") + "đ"
    except:
        return value