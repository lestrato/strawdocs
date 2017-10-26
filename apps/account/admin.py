from django.contrib import admin
from account.models import *

class AccountRecoveryStringAdmin(admin.ModelAdmin):
    list_display = ('recovery_string','created_for','created_on',)
    readonly_fields=('created_on',)
    pass
admin.site.register(AccountRecoveryString, AccountRecoveryStringAdmin)
