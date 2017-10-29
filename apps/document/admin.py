from django.contrib import admin
from document.models import *

class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'created_on',)
    readonly_fields=('created_on',)
    pass
admin.site.register(Document, DocumentAdmin)

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('document', 'title', 'created_on',)
    readonly_fields=('created_on',)
    pass
admin.site.register(Question, QuestionAdmin)

class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'created_on',)
    readonly_fields=('created_on',)
    pass
admin.site.register(Answer, AnswerAdmin)

class ReplyAdmin(admin.ModelAdmin):
    list_display = ('slug', 'post', 'created_on',)
    readonly_fields=('created_on',)
    pass
admin.site.register(Reply, ReplyAdmin)

class VoteAdmin(admin.ModelAdmin):
    list_display = ('post', 'created_by','vote_type',)
    pass
admin.site.register(Vote, VoteAdmin)
