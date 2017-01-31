from django import template
from datetime import datetime
register = template.Library()

@register.filter
def format_date(value):
    month = value.strftime("%b")
    day = value.strftime("%d")
    year = value.strftime("%Y")[-2:]
    hour = value.strftime("%H")
    minute = value.strftime("%M")

    return month + " " + day + " '" + year + " at " + hour + ":" + minute
