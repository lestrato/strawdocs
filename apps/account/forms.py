from django import forms

class EmailRecoveryForm(forms.Form):
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                 'required':'True',
                 'class': 'form-control',
                 'placeholder':'email address',
            }
        )
    )

class PasswordResetForm(forms.Form):
    username=forms.CharField(
        widget=forms.TextInput(
            attrs={
                "required":True,
                "maxlength":20,
                "class":"form-control",
                "placeholder":"Username",
                "type":"text",
            }
        ),
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "required":True,
                "class":"form-control",
                "placeholder":"Password",
                "type":"password",
                "render_value":False,
            }
        ),
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "required":True,
                "class":"form-control",
                "placeholder":"Password again",
                "type":"password",
                "render_value":False,
            }
        ),
    )

class PasswordChangeForm(forms.Form):
    current_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "required":True,
                "class":"form-control input-sm",
                "placeholder":"Current password",
                "type":"password",
                "render_value":False,
            }
        ),
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "required":True,
                "class":"form-control input-sm",
                "placeholder":"New password",
                "type":"password",
                "render_value":False,
            }
        ),
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "required":True,
                "class":"form-control input-sm",
                "placeholder":"New password confirm",
                "type":"password",
                "render_value":False,
            }
        ),
    )

class EmailChangeForm(forms.Form):
    email = forms.CharField(
        widget=forms.TextInput(
            attrs={
                 'required':True,
                 'class': 'form-control input-sm',
                 'placeholder':'new email address',
                 "type":"email",
            }
        )
    )