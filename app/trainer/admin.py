from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Regulation,ExplanationOfTask,Task

class RegulationAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)
    list_display = ['title', 'content']
    list_display_links = ['title']
    search_fields = ['title']

class ExplanationOfTaskAdmin(SummernoteModelAdmin):
    list_display = ['explanation', 'rule']
    list_display_links = ['explanation']

class TaskAdmin(SummernoteModelAdmin):
    list_display = ['question', 'answer','explanation']
    list_display_links = ['question', 'answer']

admin.site.register(Regulation, RegulationAdmin)
admin.site.register(ExplanationOfTask,ExplanationOfTaskAdmin)
admin.site.register(Task,TaskAdmin)