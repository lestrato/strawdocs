from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils import timezone

from basesite.views import *
from document.models import *
from document.forms import *

class Home(BaseView):
    def get_fetch(self, request):
        if request.user.is_authenticated():
            self.template_to_view = 'index.html'

            documents_managed = Document.objects.filter(
                created_by=request.user
            )
            self.template_items['documents_managed'] = documents_managed
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
    def get(self, request, doc_slug):
        self.template_to_view = 'overview.html'
        # this document, based on slug
        try:
           document = Document.objects.get(slug=doc_slug)
        except Document.DoesNotExist:
            # replace "with page does not exist" page
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

        questions = Question.objects.filter(
            document=document,
        )

        self.template_items['questions'] = questions
        self.template_items['document'] = document

        LIForm = LogInForm()
        SUForm = SignUpForm()

        self.template_items['LIForm'] = LIForm
        self.template_items['SUForm'] = SUForm
        self.template_items['user'] = request.user

        return render(request, self.template_to_view, self.template_items)

class QuestionView(BaseView):
    def get(self, request, doc_slug, question_url):
        self.template_to_view = 'question.html'
        # this document, based on slug
        try:
           document = Document.objects.get(slug=doc_slug)
        except Document.DoesNotExist:
            # replace "with page does not exist" page
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

        # parse the question url into a question title by changing underscores
        # to spaces
        question_title = question_url.replace ("_", " ")
        try:
            question = Question.objects.get(
                document=document,
                title = question_title,
            )
        except Question.DoesNotExist:
            # redirect to page not found, temporarily the home page
            raise Http404("Question does not exist")

        # update the question hits
        question.hits += 1
        question.save()

        # update the user's last visit time
        try:
            last_visit = UserQuestionLastVisit.objects.get(
                question=question,
                visitor=request.user,
            )
            last_visit.created_on = timezone.now()
            last_visit.save()
        except UserQuestionLastVisit.DoesNotExist:
            # first time visiting the question, create a new visit instance
            new_visit = UserQuestionLastVisit(
                question = question,
                visitor = request.user,
            )
            new_visit.save()


        self.template_items['question'] = question

        answers = Answer.objects.filter(
            question=question,
        )

        self.template_items['answers'] = answers

        ACForm = AnswerCreationForm()
        PCForm = PostCreationForm()
        self.template_items['ACForm'] = ACForm
        self.template_items['PCForm'] = PCForm

        LIForm = LogInForm()
        SUForm = SignUpForm()

        self.template_items['LIForm'] = LIForm
        self.template_items['SUForm'] = SUForm
        self.template_items['user'] = request.user

        return render(request, self.template_to_view, self.template_items)

    def post(self, request, **kwargs):
        print request.POST
        # pass
        doc_slug = kwargs.get('doc_slug', None)
        question_url = kwargs.get('question_url', None)
        try:
           document = Document.objects.get(slug=doc_slug)
        except Document.DoesNotExist:
            # replace "with page does not exist" page
            raise Http404("Document does not exist")

        # parse the question url into a question title by changing underscores
        # to spaces
        question_title = question_url.replace ("_", " ")
        try:
            question = Question.objects.get(
                document=document,
                title = question_title,
            )
        except Question.DoesNotExist:
            # redirect to page not found, temporarily the home page
            raise Http404("Question does not exist")


        if 'createAnswerSubmit' in request.POST:
            ACForm = AnswerCreationForm(request.POST)
            if ACForm.is_valid():
                # create new answer
                new_answer = Answer(
                    content=ACForm.cleaned_data['content'],
                    created_by=request.user,
                    question=question,
                )
                new_answer.save()

        if 'createReplySubmit' in request.POST:
            PCForm = PostCreationForm(request.POST)
            if PCForm.is_valid():
                # fetch the question or answer object based on the thread_slug
                thread_slug = request.POST["thread_slug"]
                try:
                    thread_object = Question.objects.get(slug=thread_slug)
                except Question.DoesNotExist:
                    try:
                        thread_object = Answer.objects.get(slug=thread_slug)
                    except Answer.DoesNotExist:
                        raise Http404("Post does not exist")
                # create new reply object
                new_reply = Reply(
                    content=PCForm.cleaned_data['content'],
                    created_by=request.user,
                    content_object=thread_object,
                )
                new_reply.save()

        if 'upvoteSubmit' in request.POST:
            print 'upvote!'
            object_slug = request.POST["upvoteSubmit"]
            try:
                this_object = Question.objects.get(slug=object_slug)
            except Question.DoesNotExist:
                try:
                    this_object = Answer.objects.get(slug=object_slug)
                except Answer.DoesNotExist:
                    try:
                        this_object = Reply.objects.get(slug=object_slug)
                    except Reply.DoesNotExist:
                        raise Http404("Post does not exist")
            try: # check if the user has upvoted this already
                upvote = this_object.upvotes.get (
                    created_by=request.user,
                )
                upvote.delete()
            except Upvote.DoesNotExist:
                try: # check if the user has downvoted this already
                    downvote = this_object.downvotes.get (
                        created_by=request.user,
                    )
                    downvote.delete()
                except Downvote.DoesNotExist:
                    pass
                # create new upvote object
                new_upvote = Upvote(
                    created_by=request.user,
                    content_object=this_object,
                )
                new_upvote.save()

        if 'downvoteSubmit' in request.POST:
            print 'downvote!'
            object_slug = request.POST["downvoteSubmit"]
            try:
                this_object = Question.objects.get(slug=object_slug)
            except Question.DoesNotExist:
                try:
                    this_object = Answer.objects.get(slug=object_slug)
                except Answer.DoesNotExist:
                    try:
                        this_object = Reply.objects.get(slug=object_slug)
                    except Reply.DoesNotExist:
                        raise Http404("Post does not exist")
            try: # check if the user has downvoted this already
                downvote = this_object.downvotes.get (
                    created_by=request.user,
                )
                downvote.delete()
            except Downvote.DoesNotExist:
                try: # check if the user has upvoted this already
                    upvote = this_object.upvotes.get (
                        created_by=request.user,
                    )
                    upvote.delete() # remove it
                except Upvote.DoesNotExist:
                    pass
                # create new downvote object
                new_downvote = Downvote(
                    created_by=request.user,
                    content_object=this_object,
                )
                new_downvote.save()

        if 'LogInFormSubmit' in request.POST:
            self.logInFormSubmit(request)

        if 'SignUpFormSubmit' in request.POST:
            self.signUpFormSubmit(request)

        return HttpResponseRedirect('/')
