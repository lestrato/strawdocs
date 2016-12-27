from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from basesite.views import *
from document.models import *
from document.forms import *

class Home(BaseView):
    def get_fetch(self, request):
        if request.user.is_authenticated():
            self.template_to_view = 'index.html'
        else:
            self.template_to_view = 'about.html'

@method_decorator(login_required, name='dispatch')
class CreateDocument(BaseView):
    def post_fetch(self, request):
        if 'createDocumentSubmit' in request.POST:
            '''
            This method is probably better than a formset, since we
            don't know how many questions the user wants to create
            '''
            to_clean_questions = []
            valid_questions = []
            # first, pair the question titles and their respective question contents
            for pair in zip(request.POST.getlist('q_title'), request.POST.getlist('content')):
                # now, create makeshift POST request data
                curr_question = {}
                curr_question['q_title'] = pair[0]
                if not pair[1]:
                    # if the user left the content field blank, then just populate it with a status message
                    curr_question['content'] = '<p>there isn\'t anything here yet.</p>'
                else:
                    curr_question['content'] = pair[1]
                to_clean_questions.append(curr_question)

            for to_clean_question in to_clean_questions:
                # send each makeshift POST request data to validate
                QCForm = QuestionCreationForm(to_clean_question)
                if QCForm.is_valid():
                    valid_questions.append((QCForm.cleaned_data['q_title'],QCForm.cleaned_data['content']))

            # check if at least one question was valid
            if len(valid_questions) >= 1:
                # check document title post data
                DCForm = DocumentCreationForm(request.POST)
                if DCForm.is_valid():
                    # we can now create a document
                    new_document = Document(
                        title=DCForm.cleaned_data['d_title'],
                        created_by=request.user,
                    )
                    new_document.save()
                    # and create questions under this document
                    for valid_question in valid_questions:
                        new_question = Question(
                            title=valid_question[0],
                            content=valid_question[1],
                            created_by=request.user,
                            document=new_document,
                        )
                        new_question.save()

    def get_fetch(self, request):
        self.template_to_view = 'create.html'
        DCForm = DocumentCreationForm()
        QCForm = QuestionCreationForm()

        self.template_items['DCForm'] = DCForm
        self.template_items['QCForm'] = QCForm

class DocumentOverview(BaseView):
    def get_fetch(self, request):
        self.template_to_view = 'overview.html'

    #  this does nothing atm
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
