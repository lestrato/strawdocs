from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, Http404, HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.db.models import Count

from basesite.decorators import login_required
from basesite.views import *
from document.models import *
from document.forms import *

def fetch_document(slug):
    try:
       return Document.objects.get(slug=slug)
    except Document.DoesNotExist:
        # replace "with page does not exist" page
        return None


def fetch_question(document, slug):
    try:
        return Question.objects.get(
            document=document,
            slug=slug,
        )
    except Question.DoesNotExist:
        # redirect to page not found, temporarily the home page
        return None

class Home(BaseView):
    def get_fetch(self, request, template_items):
        if request.user.is_authenticated():
            documents_managed = request.user.document_set.all()
            user_document_followings = request.user.userdocumentfollowing_set.all()

            template_items['documents_managed'] = documents_managed
            template_items['user_document_followings'] = user_document_followings
            return render(request, 'index.html', template_items)

        else:
            password_reset = request.GET.get('password_reset', None)
            if password_reset and password_reset == 'success':
                template_items['password_reset'] = True
            return render(request, 'about.html', template_items)

    def post_fetch(self, request):
        print request.POST
        if 'deleteDocumentSubmit' in request.POST:
            '''
            Delete the document, if the user is a manager (creator) of it
            '''
            # check if the user created the document
            try:
               document = Document.objects.get(
                    slug=request.POST['doc_slug'],
                    created_by=request.user,
                )
            except Document.DoesNotExist:
                # replace "with page does not exist" page
                return HttpResponseRedirect('/404')
            document.delete()

        if 'removeFavouriteSubmit' in request.POST:
            # first fetch the document
            try:
               document = Document.objects.get(
                    slug=request.POST['removeFavouriteSubmit'],
                )
            except Document.DoesNotExist:
                # replace "with page does not exist" page
                return HttpResponseRedirect('/404')

            try: # check if the user is following this document already
                existing_following = UserDocumentFollowing.objects.get(
                    user=request.user,
                    document=document,
                )
                existing_following.delete()

            except UserDocumentFollowing.DoesNotExist: # if not, create a new following instance
                return HttpResponseRedirect('/404')

        return HttpResponseRedirect('/')

@method_decorator(login_required, name='dispatch')
class CreateDocument(BaseView):
    def get_fetch(self, request, template_items):
        DCForm = DocumentCreationForm()
        QCForm = QuestionCreationForm()

        template_items['DCForm'] = DCForm
        template_items['QCForm'] = QCForm
        return render(request, 'create.html', template_items)

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
                    curr_question['content'] = 'there isn\'t anything here yet.'
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

        return HttpResponseRedirect('/')

class DocumentOverview(BaseView):
    def get_fetch(self, request, template_items, **kwargs):
        doc_slug = kwargs.get('doc_slug', None)
        # this document, based on slug
        document = fetch_document(slug=doc_slug)

        if not document:
            return HttpResponseRedirect('/404')

        questions = Question.objects.filter(
            document=document,
        )

        QCForm = QuestionCreationForm()

        template_items['questions'] = questions
        template_items['document'] = document
        template_items['QCForm'] = QCForm

        return render(request, 'overview.html', template_items)

    def post_fetch(self, request, **kwargs):
        doc_slug = kwargs.get('doc_slug', None)
        try:
           document = Document.objects.get(slug=doc_slug)
        except Document.DoesNotExist:
            # replace "with page does not exist" page
            return HttpResponseRedirect('/')

        if 'changeFavouriteSubmit' in request.POST:
            try: # check if the user is following this document already
                existing_following = UserDocumentFollowing.objects.get(
                    user=request.user,
                    document=document,
                )
                existing_following.delete()

            except UserDocumentFollowing.DoesNotExist: # if not, create a new following instance
                new_following = UserDocumentFollowing(
                    user=request.user,
                    document=document,
                )
                new_following.save()

        # check if user is the document creator
        if request.user == document.created_by:
            if 'createQuestionSubmit' in request.POST:
                question = {}
                question['q_title'] = request.POST['q_title']
                if not request.POST['content']:
                    question['content'] = 'there isn\'t anything here yet.'
                else:
                    question['content'] = request.POST['content']
                QCForm = QuestionCreationForm(question)

                if QCForm.is_valid():
                    new_question = Question(
                        title=QCForm.cleaned_data['q_title'],
                        content=QCForm.cleaned_data['content'],
                        created_by=request.user,
                        document=document,
                    )
                    new_question.save()

            if 'deleteQuestionSubmit' in request.POST:
                # get question based on slug
                try:
                    question = Question.objects.get(
                        document=document,
                        slug=request.POST.get('deleteQuestionSubmit', None),
                    )
                    question.delete()
                except Question.DoesNotExist:
                    # redirect to page not found, temporarily the home page
                    pass


        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

class QuestionView(BaseView):
    def get_fetch(self, request, template_items, **kwargs):
        doc_slug = kwargs.get('doc_slug', None)
        question_slug = kwargs.get('question_url', None)

        # this document, based on slug
        document = fetch_document(slug=doc_slug)

        if not document:
            return HttpResponseRedirect('/404')

        # parse the question url into a question title by changing underscores to spaces
        # this question, based on title
        question = fetch_question(document=document, slug=question_slug)

        if not question:
            return HttpResponseRedirect('/404')

        # update the question hits
        question.hits += 1
        question.save()

        # get sortby filter
        sortby = request.GET.get('sortby', False)
        if sortby and sortby == 'active' or sortby == 'votes' or sortby == 'newest':
            if request.GET['sortby'] == 'active':
                answers = Answer.objects.filter(
                    question=question,
                ).annotate(
                    num_posts=Count('replies'),
                ).order_by('-num_posts')
            elif request.GET['sortby'] == 'votes':
                answers = Answer.objects.filter(
                    question=question,
                ).annotate(
                    net_votes=(Count('upvotes')-Count('downvotes')),
                ).order_by('-net_votes')
            elif request.GET['sortby'] == 'newest':
                answers = Answer.objects.filter(
                    question=question,
                ).order_by('-created_on')
        else:
            answers = Answer.objects.filter(
                question=question,
            ).order_by('created_on')

        if not request.user.is_anonymous():
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

        PCForm = PostCreationForm()

        template_items['PCForm'] = PCForm

        template_items['document'] = document
        template_items['document_url'] = '/doc/' + document.slug
        template_items['question'] = question
        template_items['answers'] = answers
        return render(request, 'question.html', template_items)

    def post_fetch(self, request, **kwargs):
        print request.POST
        if request.user.is_anonymous():
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

        doc_slug = kwargs.get('doc_slug', None)
        question_slug = kwargs.get('question_url', None)

        # this document, based on slug
        document = fetch_document(slug=doc_slug)

        if not document:
            return HttpResponseRedirect('/404')

        # parse the question url into a question title by changing underscores to spaces
        # this question, based on title
        question = fetch_question(document=document, slug=question_slug)

        if not question:
            return HttpResponseRedirect('/404')

        if 'createAnswerSubmit' in request.POST:
            PCForm = PostCreationForm(request.POST)
            if PCForm.is_valid():
                # create new answer
                new_answer = Answer(
                    content=PCForm.cleaned_data['content'],
                    created_by=request.user,
                    question=question,
                )
                new_answer.save()

        if 'createReplySubmit' in request.POST:
            PCForm = PostCreationForm(request.POST)
            if PCForm.is_valid():
                # fetch the question or answer object based on the thread_slug
                thread_slug = request.POST["createReplySubmit"]
                try:
                    thread_object = Question.objects.get(slug=thread_slug)
                except Question.DoesNotExist:
                    try:
                        thread_object = Answer.objects.get(slug=thread_slug)
                    except Answer.DoesNotExist:
                        raise Http404("Post does not exist")

                # check if this reply object exists already
                # create new reply object
                new_reply = Reply(
                    content=PCForm.cleaned_data['content'],
                    created_by=request.user,
                    content_object=thread_object,
                )
                new_reply.save()

        if 'upvoteSubmit' in request.POST:
            object_slug = request.POST["upvoteSubmit"]
            post_type = None
            try:
                this_object = Question.objects.get(slug=object_slug)
            except Question.DoesNotExist:
                try:
                    this_object = Answer.objects.get(slug=object_slug)
                except Answer.DoesNotExist:
                    try:
                        this_object = Reply.objects.get(slug=object_slug)
                        post_type = 'reply'
                    except Reply.DoesNotExist:
                        error_message = 'The post does not exist anymore.'
                        ReplyNotExistError = {'error': error_message}
                        return JsonResponse(ReplyNotExistError)

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

            return render(request, 'post.html', {'post':this_object,  'post_type':post_type})

        if 'downvoteSubmit' in request.POST:
            object_slug = request.POST["downvoteSubmit"]
            post_type = None
            try:
                this_object = Question.objects.get(slug=object_slug)
            except Question.DoesNotExist:
                try:
                    this_object = Answer.objects.get(slug=object_slug)
                except Answer.DoesNotExist:
                    try:
                        this_object = Reply.objects.get(slug=object_slug)
                        post_type = 'reply'
                    except Reply.DoesNotExist:
                        error_message = 'The post does not exist anymore.'
                        ReplyNotExistError = {'error': error_message}
                        return JsonResponse(ReplyNotExistError)

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

            return render(request, 'post.html', {'post':this_object,  'post_type':post_type})

        if 'editPostSubmit' in request.POST:
            # fetch post by slug
            print request.POST
            pass
            try:
                old_post = Question.objects.get(slug=request.POST['editPostSubmit'])
            except Question.DoesNotExist:
                try:
                    old_post = Answer.objects.get(slug=request.POST['editPostSubmit'])
                except Answer.DoesNotExist:
                    raise Http404("Post does not exist")

            # check to make sure user is the one who created it
            if request.user == old_post.created_by:
                PCForm = PostCreationForm(request.POST)
                if PCForm.is_valid():
                    # now change the content
                    old_post.content = PCForm.cleaned_data['content']
                    old_post.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
