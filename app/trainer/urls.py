from django.urls import path
from . import views

urlpatterns = [
 path('', views.index, name='index'),
 path('dashboard/', views.dashboard, name='dashboard'),
 path('dashboard/dictionary/', views.dictionary, name='dictionary'),
 path('dashboard/rules/', views.by_rule, name='list_of_rules'),
 path('dashboard/rules/<int:rules_id>', views.text_rules, name='full_rules'),
]
