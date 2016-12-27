from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.views import View

from basesite.forms import *

class BaseView(View):
    """ To be inherited by every view """
    def __init__(self):
        self.template_items = {}

    def post_fetch(self, request):
        pass

    def get_fetch(self, request):
        pass

    def my_authenticate(self, username, password):
        return authenticate(username=username, password=password)

    def logInFormSubmit(self, request):
        LIForm = LogInForm(request.POST)
        if LIForm.is_valid():
            user = self.my_authenticate(
                username=LIForm.cleaned_data['username'],
                password=LIForm.cleaned_data['password']
            )
            if user:
                login(request, user)

    def signUpFormSubmit(self, request):
        SUForm = SignUpForm(request.POST)
        if SUForm.is_valid():
            user = User.objects.create_user(
                username=SUForm.cleaned_data['username'],
                password=SUForm.cleaned_data['password1'],
                email=SUForm.cleaned_data['email']
            )
            user = self.my_authenticate(
                username=SUForm.cleaned_data['username'],
                password=SUForm.cleaned_data['password1']
            )
            if user:
                login(request, user)

    def post(self, request):
        """ Fetch the post request from the extended veiw class"""
        self.post_fetch(request)
        if 'LogInFormSubmit' in request.POST:
            self.logInFormSubmit(request)

        if 'SignUpFormSubmit' in request.POST:
            self.signUpFormSubmit(request)

        return HttpResponseRedirect('.')

    def get(self, request):
        """ Fetch the get request from the extended veiw class"""
        self.get_fetch(request)

        LIForm = LogInForm()
        SUForm = SignUpForm()

        self.template_items['LIForm'] = LIForm
        self.template_items['SUForm'] = SUForm
        self.template_items['user'] = request.user

        return render(request, self.template_to_view, self.template_items)

def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')
