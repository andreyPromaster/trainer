from django.contrib import admin

from .models import Regulation,ExplanationOfTask,Task
class RegulationAdmin(admin.ModelAdmin):
	list_display = ['title', 'content']
	list_display_links = ['title']
	search_fields = ['title']

class ExplanationOfTaskAdmin(admin.ModelAdmin):
    list_display = ['explanation', 'rule']
    list_display_links = ['explanation']

class TaskAdmin(admin.ModelAdmin):
    list_display = ['question', 'answer','explanation']
    list_display_links = ['question', 'answer']

admin.site.register(Regulation, RegulationAdmin)
admin.site.register(ExplanationOfTask,ExplanationOfTaskAdmin)
admin.site.register(Task,TaskAdmin)