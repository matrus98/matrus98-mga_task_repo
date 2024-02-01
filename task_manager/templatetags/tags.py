from django import template
register = template.Library()


@register.filter
def index(row, i):
    try:
        return row[i]
    except IndexError:
        return ''
