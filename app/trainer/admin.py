from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Regulation, Quiz, Task, Answer, TakenQuiz, StudentAnswer, Student

class RegulationAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)
    list_display = ['title', 'content']
    list_display_links = ['title']
    search_fields = ['title']

class QuizAdmin(SummernoteModelAdmin):
    summernote_fields = ('explanation',)
    list_display = ['explanation', 'rule', 'name' ]
    list_display_links = ['explanation']

class TaskAdmin(SummernoteModelAdmin):
    summernote_fields = ('question',)
    list_display = ['question','quiz']
    list_display_links = ['question', 'quiz']

class AnswerAdmin(admin.ModelAdmin):
    list_display = ['question','text', 'is_correct']
    list_display_links = ['question']

class StudentAdmin(admin.ModelAdmin):
    list_display = ['user']
    list_display_links = ['user']

class TakenQuiztAdmin(admin.ModelAdmin):
    list_display = ['student','quiz', 'score','date']
    list_display_links = ['student','quiz','date']

class StudentAnswerAdmin(admin.ModelAdmin):
    list_display = ['student','answer','taken_quiz']
    list_display_links = ['student','answer','taken_quiz']


admin.site.register(Regulation, RegulationAdmin)
admin.site.register(Quiz,QuizAdmin)
admin.site.register(Task,TaskAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(TakenQuiz, TakenQuiztAdmin)
admin.site.register(StudentAnswer, StudentAnswerAdmin)