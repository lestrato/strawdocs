from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import user_passes_test

def login_forbidden(function=None, redirect_field_name=None, redirect_to='/account/'):
    """
    Decorator for views that checks that the user is NOT logged in, redirecting
    to the homepage if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: not u.is_authenticated(),
        login_url=redirect_to,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)

    return actual_decorator

def login_required(function):
    def wrapper(request, *args, **kw):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/?next='+request.get_full_path())
        else:
            return function(request, *args, **kw)
    return wrapper
