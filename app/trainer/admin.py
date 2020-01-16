from django.contrib import admin

from .models import Regulation,ExplanationOfTask,Task
admin.site.register(Regulation)
admin.site.register(ExplanationOfTask)
admin.site.register(Task)