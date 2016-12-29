from django import template

register = template.Library()

@register.filter
def str_to_int(string):
    return int(string)
