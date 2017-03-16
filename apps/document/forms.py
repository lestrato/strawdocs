from django import forms

class DocumentCreationForm(forms.Form):
    d_title = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'required':'True',
                'class': 'form-control document-title-input',
                 'maxlength':'30',
                 'placeholder':'Document Title',
            }
        )
    )
class QuestionCreationForm(forms.Form):
    q_title = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'required':'True',
                'class': 'form-control question-title-input',
                'placeholder':'Question Title',
                'maxlength':'30',
            }
        )
    )
    content = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'id': 'create-question-editor',
            }
        )
    )
class PostCreationForm(forms.Form):
    content = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'id': 'create-post-editor',
            }
        )
    )
