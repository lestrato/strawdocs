import re
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class LogInForm(forms.Form):
    username=forms.CharField(
        widget=forms.TextInput(
            attrs={
                "required":True,
                "maxlength":20,
                "class":"form-control input-sm",
                "placeholder":"Username",
                "type":"text",
            }
        ),
    )
    password=forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(
            attrs={
                "required":True,
                "class":"form-control input-sm",
                "placeholder":"Password",
                "type":"password",
            }
        )
    )

class SignUpForm(forms.Form):
    username = forms.RegexField(
        regex=r'^\w+$', widget=forms.TextInput(
            attrs={
                "required":True,
                "maxlength":20,
                "class":"form-control input-sm",
                "placeholder":"Username",
                "type":"text",
            }
        ),
        label=_("Username"),
        error_messages={ 'invalid': _("This value must contain only letters, numbers and underscores.") }
    )
    email = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "required":True,
                "class":"form-control input-sm",
                "placeholder":"Email",
                "type":"email",
            }
        ),
        label=_("Email address")
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "required":True,
                "class":"form-control input-sm",
                "placeholder":"Password",
                "type":"password",
                "render_value":False,
            }
        ),
        label=_("Password")
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "required":True,
                "class":"form-control input-sm",
                "placeholder":"Password again",
                "type":"password",
                "render_value":False,
            }
        ),
        label=_("Password (again)")
    )
