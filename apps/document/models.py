from __future__ import unicode_literals

from django.db import models

from randomslugfield import RandomSlugField
from tinymce import models as tinymce_models

class Document(models.Model):
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

    def __str__(self):
        return self.title

class Question(models.Model):
    document = models.ForeignKey(
        'Document',
        on_delete=models.CASCADE,
    )
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
    def __str__(self):
        return self.title
