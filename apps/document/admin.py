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

class ReportPostAdmin(admin.ModelAdmin):
    list_display = ('user', 'report_post__post', 'created_on','resolved',)

    def report_post__post(self, obj):
        return obj.post.slug
    report_post__post.admin_order_field  = 'post__slug'  #Allows column order sorting
    report_post__post.short_description = 'Post Slug'  #Renames column head
    pass
admin.site.register(ReportPost, ReportPostAdmin)

class ReportPostReasonAdmin(admin.ModelAdmin):
    list_display = ('report_post__post', 'report_choice',)

    def report_post__post(self, obj):
        return obj.report_post.post.slug
    report_post__post.admin_order_field  = 'report_post__post__slug'  #Allows column order sorting
    report_post__post.short_description = 'Post Slug'  #Renames column head
    pass
admin.site.register(ReportPostReason, ReportPostReasonAdmin)
