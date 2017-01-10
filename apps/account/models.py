from __future__ import unicode_literals

from django.db import models
from django.conf import settings

class AccountRecoveryString(models.Model):
    ''' Every account recovery string has:
    - a recovery_string (unhashed)
    - a user it's created for
    - a datetime it was created on
    '''
    recovery_string = models.CharField(
        blank=False,
        max_length=50,
    )
    created_for = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=False,
    )
    created_on = models.DateTimeField(
        auto_now_add=True,
        blank=False,
    )
