from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist

from randomslugfield import RandomSlugField
from simplemde.fields import SimpleMDEField

class Document(models.Model):
    ''' Every document has:
    - a title
    - a slug to be used as the url and identifier
    - a date it was created on
    < a user it was created by
    < a set of moderators, one of which is a the creator
    > a set of questions
    '''
    title = models.CharField(
        max_length=30,
        blank=False,
    )
    slug = RandomSlugField(
        length=7,
        blank=False,
        unique=True,
    )
    created_on = models.DateField(
        auto_now_add=True,
        blank=False,
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=False,
    )
    moderators = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='document_moderator'
    )

    def __str__(self):
        return self.title

class Post(models.Model):
    ''' Every post has:
    - a slugfield
    - content
    - a datetime it was created on
    - a user it was created by
    '''
    slug = RandomSlugField(
        length=8,
        blank=False,
        unique=True,
    )
    content = SimpleMDEField(
        blank=False,
    )
    created_on = models.DateTimeField(
        auto_now_add=True,
        blank=False,
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=False
    )

    def child(self):
        for subclass in self.__class__.__subclasses__():
            try:
                return getattr(self, subclass.__name__.lower())
            except (AttributeError, ObjectDoesNotExist):
                continue

    def upvotes(self):
        return Vote.objects.filter(post=self, vote_type='upvote')

    def downvotes(self):
        return Vote.objects.filter(post=self, vote_type='downvote')

class Vote(models.Model):
    ''' Every vote has:
    - a type: upvote or downvote
    - a user who created it
    - a question/answer/reply it references
    '''
    VOTE_TYPES = (
        ('upvote', 'upvote'),
        ('downvote', 'downvote'),
    )
    post = models.ForeignKey(
        'Post',
        blank=False
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=False
    )
    vote_type = models.CharField(
        blank=False,
        max_length=10,
        choices=VOTE_TYPES,
    )

class Reply(Post):
    ''' Every reply is a Post and also has:
    - a number of upvotes
    < a question/answer/reply it addresses
    > a set of replies
    '''
    post = models.ForeignKey(
        'Post',
        blank=False,
        related_name='post_reply'
    )

class Question(Post):
    ''' Every question is a Post and also has:
    - a title
    - a number of upvotes
    - a number of downvotes
    < a document it belongs to
    > a set of replies
    '''
    title = models.CharField(
        max_length=30,
        blank=False,
    )
    document = models.ForeignKey(
        'Document',
        on_delete=models.CASCADE,
    )
    hits = models.IntegerField(
        default=0,
        blank=False,
    )

    def __str__(self):
        return self.title

class Answer(Post):
    ''' Every answer is a Post and also has:
    - a number of upvotes
    - a number of downvotes
    < a question it belongs to
    > a set of replies
    '''
    parent_question = models.ForeignKey(
        'Question',
        on_delete=models.CASCADE,
        related_name='question_answer',
    )
    def __str__(self):
        return self.question.title

class UserQuestionLastVisit(models.Model):
    ''' Every user's last visit to a question has:
    < a user who visited it
    < a question
    - a date when it happened
    '''
    visitor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=False
    )
    question = models.ForeignKey(
        'Question',
        on_delete=models.CASCADE,
    )
    created_on = models.DateTimeField(
        auto_now_add=True,
        blank=False,
    )

class UserDocumentFollowing(models.Model):
    ''' Every document the user follows has:
    < a user who follows it
    < a document
    '''
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=False
    )
    document = models.ForeignKey(
        'Document',
        on_delete=models.CASCADE,
    )
