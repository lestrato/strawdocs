from __future__ import unicode_literals

from django.db import models
from django.conf import settings

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

class Question(models.Model):
    ''' Every question has:
    - a title
    - a question content
    - a date it was created on
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
    created_on = models.DateField(
        auto_now_add=True,
        blank=False,
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=False
    )
    upvotes = models.IntegerField(
        default=0,
        blank=False,
    )
    downvotes = models.IntegerField(
        default=0,
        blank=False,
    )
    document = models.ForeignKey(
        'Document',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.title
