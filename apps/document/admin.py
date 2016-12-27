from django.contrib import admin
from document.models import Document, Question

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
