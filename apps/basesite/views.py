from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, JsonResponse
from django.views import View
from django.template import RequestContext

from basesite.forms import *

class BaseView(View):
    """ To be inherited by every view """
    def logInFormSubmit(self, request):
        LIForm = LogInForm(request.POST)
        if LIForm.is_valid():
            user = authenticate(
                username=LIForm.cleaned_data['username'],
                password=LIForm.cleaned_data['password']
            )
            if user:
                login(request, user)
            else:
                return

    def signUpFormSubmit(self, request):
        SUForm = SignUpForm(request.POST)
        if SUForm.is_valid():
            user = User.objects.create_user(
                username=SUForm.cleaned_data['username'],
                password=SUForm.cleaned_data['password1'],
                email=SUForm.cleaned_data['email']
            )
            user = authenticate(
                username=SUForm.cleaned_data['username'],
                password=SUForm.cleaned_data['password1']
            )
            if user:
                login(request, user)

    def get_fetch(self, request, *args, **kwargs):
        ''' To be overridden '''
        pass

    def get(self, request, *args, **kwargs):
        template_items = {}

        LIForm = LogInForm()
        SUForm = SignUpForm()
        template_items['LIForm'] = LIForm
        template_items['SUForm'] = SUForm
        template_items ['user'] = request.user

        return self.get_fetch(request, template_items, *args, **kwargs)

    def post_fetch(self, request, *args, **kwargs):
        ''' To be overridden '''
        pass

    def post(self, request, *args, **kwargs):
        if 'LogInFormSubmit' in request.POST:
            LIForm = LogInForm(request.POST)
            if LIForm.is_valid():
                user = authenticate(
                    username=LIForm.cleaned_data['username'],
                    password=LIForm.cleaned_data['password']
                )
                if user:
                    login(request, user)
                else:
                    return JsonResponse({'error_message': 'Wrong credentials were inputted (both fields are case-sensitive.)'})

        if 'SignUpFormSubmit' in request.POST:
            SUForm = SignUpForm(request.POST)
            if SUForm.is_valid():
                if User.objects.get(username__iexact=SUForm.cleaned_data['username']):
                    return JsonResponse({'error_message': 'The username already exists. Please try another one.'})
                if SUForm.cleaned_data['password1'] != SUForm.cleaned_data['password2']:
                    return JsonResponse({'error_message': 'The two password fields did not match.'})
                user = User.objects.create_user(
                    username=SUForm.cleaned_data['username'],
                    password=SUForm.cleaned_data['password1'],
                    email=SUForm.cleaned_data['email']
                )
                user = authenticate(
                    username=SUForm.cleaned_data['username'],
                    password=SUForm.cleaned_data['password1']
                )
                if user:
                    login(request, user)

        return self.post_fetch(request, *args, **kwargs)

# HTTP Error 400
class bad_request(BaseView):
    def get_fetch(self, request, template_items):
        response = render(request, '400.html', template_items)
        response.status_code = 400
        return response

# HTTP Error 403
class permission_denied(BaseView):
    def get_fetch(self, request, template_items):
        response = render(request, '403.html', template_items)
        response.status_code = 403
        return response

# HTTP Error 404
class page_not_found(BaseView):
    def get_fetch(self, request, template_items):
        response = render(request, '404.html', template_items)
        response.status_code = 404
        return response

# HTTP Error 500
class server_error(BaseView):
    def get(self, request, template_items):
        response = render(request, '500.html', template_items)
        response.status_code = 500
        return response

def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')
