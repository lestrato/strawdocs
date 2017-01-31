from django import template
register = template.Library()

@register.filter
def title_to_url(title):
    return title.replace (" ", "_")
