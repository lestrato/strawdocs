from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test

from basesite.views import *

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

@method_decorator(login_required, name='dispatch')
class Settings(BaseView):
    def get_fetch(self, request, template_items):
        return render(request, 'settings.html', template_items)

    def post_fetch(self, request):
        return HttpResponseRedirect('/')

@method_decorator(login_forbidden, name='dispatch')
class Recovery(BaseView):
    def get_fetch(self, request, template_items):
        return render(request, 'recovery.html', template_items)

    def post_fetch(self, request):
        return HttpResponseRedirect('/')
