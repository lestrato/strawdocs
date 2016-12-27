from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from basesite.views import *
from document.models import *

class Home(BaseView):
    def fetch(self, request):
        if request.user.is_authenticated():
            self.template_to_view = 'index.html'
        else:
            self.template_to_view = 'about.html'

@method_decorator(login_required, name='dispatch')
class CreateDocument(BaseView):
    def fetch(self, request):
        self.template_to_view = 'create.html'


class DocumentOverview(BaseView):
    def fetch(self, request):
        self.template_to_view = 'overview.html'

    def get(self, request, doc_slug):
        """
        Check if template_to_view has been set in an extended view class
        """
        # this document, based on slug
        try:
           document = Document.objects.get(slug=doc_slug)
        except Document.DoesNotExist:
            # replace "with page does not exist" page
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

        questions = Question.objects.filter(
            document=document,
        )

        LIForm = LogInForm()
        SUForm = SignUpForm()

        return render(request, self.template_to_view, {
            'LIForm': LIForm,
            'SUForm': SUForm,
            'user': request.user,
            'document': document,
            'questions': questions,
        })
