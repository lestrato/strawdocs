from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.views import View

from basesite.forms import *

class BaseView(View):
    """ To be inherited by every view """
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
        if request.method == 'POST':
            if 'LogInFormSubmit' in request.POST:
                self.logInFormSubmit(request)

            if 'SignUpFormSubmit' in request.POST:
                self.signUpFormSubmit(request)

            return HttpResponseRedirect('/')

        return render(request, self.template_to_view, {
            'LIForm': LIForm,
            'SUForm': SUForm,
            'user': request.user,
        })

    def get(self, request):
        """
        Check if template_to_view has been set in an extended view class
        """
        self.fetch(request)

        LIForm = LogInForm()
        SUForm = SignUpForm()

        return render(request, self.template_to_view, {
            'LIForm': LIForm,
            'SUForm': SUForm,
            'user': request.user,
        })


def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')
