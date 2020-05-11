from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from .forms import FindWordForm, TakeQuizForm
import pdb
from .dictionary import Parcer
from .models import Regulation
from django.db import transaction
from django.db.models import Count, Max
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.views.generic.base import TemplateView
from .models import Quiz, Student, TakenQuiz
from django.contrib import messages
from datetime import timedelta, datetime

def index(request):
    return render(
        request,
        'index.html',
    )


class BoardTemplateView(LoginRequiredMixin, TemplateView):
    login_url = '/account/login/'
    template_name = 'dashboard.html' 


class RuleListView(LoginRequiredMixin, ListView):
    login_url = '/account/login/'
    template_name = 'list_rules.html' 
    model = Regulation
    context_object_name = 'rules' 


class SelectedRuleListView(LoginRequiredMixin, ListView):
    login_url = '/account/login/'
    template_name = 'full_rules.html' 
    model = Regulation

    def get_context_data(self, *args, **kwargs) :
        context = super() .get_context_data(*args, **kwargs)
        context['current_rule'] = get_object_or_404(Regulation, pk=self.kwargs['rules_id'])
        return context


@login_required (login_url = '/account/login/')
def dictionary(request):
    search_word = ''
    if request.method == 'POST':
        form= FindWordForm(request.POST)        
        if form.is_valid():
            search_word= form.cleaned_data['word']
            parcer = Parcer()
            search_word = parcer.getExplanationOfWord(parcer.getPageWitfoundedWord(search_word))

    else:
        form= FindWordForm()
    context= {'form': form, 'word': search_word}
    return render(request, 'dictionary.html', context)


class QuizListView(LoginRequiredMixin, ListView):
    model = Quiz
    ordering = ('name', )
    context_object_name = 'quizzes'
    template_name = 'quiz_list.html'

    def get_queryset(self):
        student = self.request.user.student   #“Аннотирует” каждый объект в QuerySet агрегированным значением (среднее, суииа и др.), которое будет вычислено из данных связанных объектов, которые связанны с объектами из``QuerySet``. 
        taken_quizzes = student.quizzes.values_list('pk', flat=True) #достаем квизы, которые еще не выполнены и кол-во вопросов больше 0
        queryset = Quiz.objects.exclude(pk__in=taken_quizzes) \
                               .annotate(questions_count=Count('questions')) \
                               .filter(questions_count__gt=0)#достаем квизы, которые были выполнены не ранее 2 часов
        old_tests = student.taken_quizzes.values('quiz').annotate(max=Max('date')) \
                               .filter(max__lt=datetime.now() - timedelta(hours=2)) \
                               .values_list('quiz', flat=True)
        print(old_tests)
        old_tests_queryset = Quiz.objects.filter(pk__in=old_tests) \
                                         .annotate(questions_count=Count('questions')).distinct()#??
        queryset = queryset.union(old_tests_queryset)
        return queryset

# в список квизов добавить, те которые старше 3 дней, перед выполнением проверить был ли этот кветс пройден ранее,
# если так, тогда удалить все ответы студента, в пройденных тестах показывать еще и дату.
class TakenQuizListView(LoginRequiredMixin, ListView):
    model = TakenQuiz
    context_object_name = 'taken_quizzes'
    template_name = 'taken_quiz_list.html'

    def get_queryset(self): #Возвращает QuerySet который автоматически включает в выборку данные связанных объектов при выполнении запроса.
        queryset = self.request.user.student.taken_quizzes.select_related('quiz').order_by('quiz__name')
        return queryset


@login_required
def take_quiz(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    student = request.user.student

    if student.quizzes.filter(pk=pk).exists(): #проверяем квизы, которые послучайности запушены, но время блокировки еще не вышло
        if student.taken_quizzes.filter(pk=pk,date__gt=datetime.now() - timedelta(hours=2)) \
                                .values_list('quiz', flat=True) \
                                .exists():
            return render(request, 'taken_quiz_list.html')

    total_questions = quiz.questions.count()
    unanswered_questions = student.get_unanswered_questions(quiz)
    total_unanswered_questions = unanswered_questions.count()
    progress = 100 - round(((total_unanswered_questions - 1) / total_questions) * 100)

    if request.method == 'POST':
        question = []
        if request.POST.get('answer') is None:
            question = unanswered_questions.first()
        else:
            for i in unanswered_questions.filter(answers__pk=request.POST['answer']):
                question = i
                  
        form = TakeQuizForm(question=question, data=request.POST)
        if form.is_valid():
            with transaction.atomic():
                student_answer = form.save(commit=False)
                student_answer.student = student
                student_answer.save()
                if student.get_unanswered_questions(quiz).exists():
                    return redirect('take_quiz', pk)
                else:
                    correct_answers = student.quiz_answers.filter(answer__question__quiz=quiz,
                                                                  taken_quiz=None,
                                                                  answer__is_correct=True).count()
                    score = round((correct_answers / total_questions) * 100.0, 2)
                    new_taken_quiz = TakenQuiz.objects.create(student=student, quiz=quiz, score=score)
                    student.quiz_answers.filter(answer__question__quiz=quiz, taken_quiz=None) \
                                               .update(taken_quiz=new_taken_quiz.pk)
                    if score < 50.0:
                        messages.warning(request, 'У наступным разе будзе лепей %s лік %s.' 
                                         % (quiz.name, score))
                    else:
                        messages.success(request, 'Мае віншаванні, %s! Твой лік %s.' % (quiz.name, score))
                    return redirect('quiz_list')
    else:
        unanswered_questions = unanswered_questions.order_by('?')    
        question = unanswered_questions.first()
        form = TakeQuizForm(question=question)

    return render(request, 'take_quiz_form.html', {
        'quiz': quiz,
        'question': question,
        'form': form,
        'progress': progress
    })
