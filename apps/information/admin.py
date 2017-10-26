from django.contrib import admin
from information.models import *

class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ('help_topic','email','created_on','resolved',)
    readonly_fields=('created_on',)
    pass
admin.site.register(SupportTicket, SupportTicketAdmin)
