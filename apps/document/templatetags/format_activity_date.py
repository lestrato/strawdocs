from django import template
from django.utils import timezone

register = template.Library()

@register.filter
def format_activity_date(last_post):
    formatted_string = 'error'
    if type(last_post).__name__ == 'Reply':
        formatted_string = 'replied '

    elif type(last_post).__name__ == 'Question':
        formatted_string = 'asked '

    elif type(last_post).__name__ == 'Answer':
        formatted_string = 'answered '

    time_difference = timezone.now() - last_post.created_on
    td_years = time_difference.days / 365
    td_months = time_difference.days / 30
    td_days = time_difference.days
    td_hours = time_difference.seconds / 3600
    td_minutes = time_difference.seconds / 60
    td_seconds = time_difference.seconds

    if td_years > 1:
        formatted_string += str(td_years) + " years ago"
    elif td_years == 1:
        formatted_string += str(td_years) + " year ago"
    elif td_months > 1:
        formatted_string += str(td_months) + " months ago"
    elif td_months == 1:
        formatted_string += str(td_months) + " month ago"
    elif td_days > 1:
        formatted_string += str(td_days) + " days ago"
    elif td_days == 1:
        formatted_string += str(td_days) + " day ago"
    elif td_hours > 1:
        formatted_string += str(td_hours) + " hours ago"
    elif td_hours == 1:
        formatted_string += str(td_hours) + " hour ago"
    elif td_minutes > 1:
        formatted_string += str(td_minutes) + " minutes ago"
    elif td_minutes == 1:
        formatted_string += str(td_minutes) + " minute ago"
    elif td_seconds > 1:
        formatted_string += str(td_seconds) + " seconds ago"
    elif td_seconds == 1:
        formatted_string += str(td_seconds) + " second ago"
    elif td_seconds == 0:
        formatted_string += " just now"
        
    return formatted_string
