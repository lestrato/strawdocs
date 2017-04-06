from __future__ import unicode_literals

from django.db import models

class SupportTicket(models.Model):
    ''' Every ticket has:
    - a help topic
    - a email of the creator
    - a name of the creator
    - the issue summary
    - the issue details
    - the datetime of creation
    - if it has been closed or not
    '''
    TOPIC_CHOICES = (
        ('feedback', 'feedback'),
        ('inquiry', 'inquiry'),
        ('report', 'report'),
    )
    help_topic = models.CharField(
        blank=False,
        max_length=100,
        choices=TOPIC_CHOICES,
    )
    email = models.EmailField(
        blank=False,
        max_length=50,
    )    
    creator_name = models.CharField(
        blank=False,
        max_length=50,
    )  
    summary = models.CharField(
        blank=False,
        max_length=100,
    )    
    details = models.TextField(
        blank=False,
    )    
    created_on = models.DateTimeField(
        auto_now_add=True,
        blank=False,
    )
    resolved = models.BooleanField(
        default=False,
        blank=False,
    )

