from django.contrib import admin
from document.models import *

class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'created_on',)
    fieldsets = (
        ('Properties', {'fields': ('title',)}),
    )
    pass
admin.site.register(Document, DocumentAdmin)

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('document', 'title', 'created_on',)
    fieldsets = (
        ('Properties', {'fields': ('document', 'title', 'content')}),
    )
    pass
admin.site.register(Question, QuestionAdmin)

class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'created_on',)
    fieldsets = (
        ('Properties', {'fields': ('question', 'content')}),
    )
    pass
admin.site.register(Answer, AnswerAdmin)

class ReplyAdmin(admin.ModelAdmin):
    list_display = ('slug', 'content_type', 'created_on',)
    fieldsets = (
        ('Properties', {'fields': ['content']}),
    )
    pass
admin.site.register(Reply, ReplyAdmin)

class UpvoteAdmin(admin.ModelAdmin):
    list_display = ('created_by',)
    fieldsets = (
        ('Properties', {'fields': ['created_by']}),
    )
    pass
admin.site.register(Upvote, UpvoteAdmin)

class DownvoteAdmin(admin.ModelAdmin):
    list_display = ('created_by',)
    fieldsets = (
        ('Properties', {'fields': ['created_by']}),
    )
    pass
admin.site.register(Downvote, DownvoteAdmin)
