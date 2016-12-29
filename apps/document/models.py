from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType

from randomslugfield import RandomSlugField
from tinymce import models as tinymce_models

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
    '''
    slug = RandomSlugField(
        length=8,
        blank=False,
        unique=True,
    )
    class Meta:
        abstract = True

class Vote(models.Model):
    ''' Every vote has:
    - a type: upvote or downvote
    - a user who created it
    - a question/answer/reply it references
    '''
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=False
    )
    #  generic foreign key to either a question/answer/reply
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        abstract = True

class Upvote(Vote):
    def __str__(self):
        return self.content_object.slug

class Downvote(Vote):
    def __str__(self):
        return self.content_object.slug

class Reply(Post):
    ''' Every reply has:
    - a reply content
    - a datetime it was created on
    - a user it was created by
    - a number of upvotes
    < a question/answer/reply it addresses
    > a set of replies
    '''
    content = tinymce_models.HTMLField(
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
    #  generic foreign key to either a question/answer/reply
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    upvotes = GenericRelation(Upvote)
    downvotes = GenericRelation(Downvote)

    def __str__(self):
        return self.content_object.slug

class Question(Post):
    ''' Every question has:
    - a title
    - a question content
    - a datetime it was created on
    - a user it was created by
    - a number of upvotes
    - a number of downvotes
    < a document it belongs to
    > a set of replies
    '''
    title = models.CharField(
        max_length=30,
        blank=False,
    )
    content = tinymce_models.HTMLField(
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
    document = models.ForeignKey(
        'Document',
        on_delete=models.CASCADE,
    )
    hits = models.IntegerField(
        default=0,
        blank=False,
    )
    replies = GenericRelation(Reply)
    upvotes = GenericRelation(Upvote)
    downvotes = GenericRelation(Downvote)

    class Meta:
        unique_together = ('title', 'document',)

    def __str__(self):
        return self.title

class Answer(Post):
    ''' Every answer has:
    - an answer content
    - a datetime it was created on
    - a user it was created by
    - a number of upvotes
    - a number of downvotes
    < a question it belongs to
    > a set of replies
    '''
    content = tinymce_models.HTMLField(
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
    question = models.ForeignKey(
        'Question',
        on_delete=models.CASCADE,
    )
    replies = GenericRelation(Reply)

    upvotes = GenericRelation(Upvote)
    downvotes = GenericRelation(Downvote)

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
