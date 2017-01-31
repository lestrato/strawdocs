from django import template
from document.models import UserDocumentFollowing
register = template.Library()

@register.filter
def is_following(document, user):
    try: # check if the user is following this document already
        document.userdocumentfollowing_set.all().get(user=user)
        return True
    except UserDocumentFollowing.DoesNotExist: # if not, create a new following instance
        return False
