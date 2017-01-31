from django import template
from django.utils import timezone
import mistune


register = template.Library()

@register.filter
def test_markdown(old_markdown):
    return mistune.markdown(old_markdown)
