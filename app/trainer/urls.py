from django.urls import path
from . import views

urlpatterns = [
 path('', views.index, name='index'),
 path('dashboard/', views.BoardTemplateView.as_view(), name='dashboard'),
 path('dashboard/dictionary/', views.dictionary, name='dictionary'),
 path('dashboard/rules/', views.RuleListView.as_view(), name='list_of_rules'),
 path('dashboard/rules/<int:rules_id>', views.SelectedRuleListView.as_view(), name='full_rules'),
 path('dashboard/quiz/', views.QuizListView.as_view(), name='quiz_list'),
 path('dashboard/taken/', views.TakenQuizListView.as_view(), name='taken_quiz_list'),
 path('dashboard/quiz/<int:pk>/', views.take_quiz, name='take_quiz'),
]

