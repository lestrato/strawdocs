from django import forms
from information.models import SupportTicket

class TicketCreationForm(forms.Form):
    topic = forms.ChoiceField(
    	choices = SupportTicket.TOPIC_CHOICES,
        widget=forms.Select(
            attrs={
                'required':'True',
                'class': 'form-control',
                'placeholder':'Question Title',
                'maxlength':'30',
            }
        )
    )
    email = forms.CharField(
        widget=forms.TextInput(
            attrs={
                 'required':'True',
                 'class': 'form-control',
                 'placeholder':'Email',
                 'maxlength':'50',
            }
        )
    )
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'required':'True',
                'class': 'form-control',
                'placeholder':'Name',
                'maxlength':'50',
            }
        )
    )
    summary = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'required':'True',
                'class': 'form-control',
                'placeholder':'Summary',
                'maxlength':'100',
            }
        )
    )
    details = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'required':'True',
                'class': 'form-control',
                'placeholder':'Start talkin!',
                'style':'resize:vertical; height: 75px;',
            }
        )
    )