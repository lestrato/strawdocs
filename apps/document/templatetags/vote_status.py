from django import template

register = template.Library()

@register.filter
def vote_status(votes, user):
    try:
        votes.get(created_by=user,)
        return True
    except Exception as e:
        return False
