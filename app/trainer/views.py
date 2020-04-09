from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import FindWordForm
import pdb
from .dictionary import Parcer
from .models import Regulation
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.views.generic.base import TemplateView

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
    #context_object_name = 'rule'
    model = Regulation

    def get_context_data(self, *args, **kwargs) :
        context = super() .get_context_data(*args, **kwargs)
        context['current_rule'] = Regulation.objects.get(pk=self.kwargs['rules_id'])
        return context

#@login_required (login_url = '/account/login/')
def dashboard(request):
    return render(
        request,
        'dashboard.html',
    )
def dictionary(request):
    search_word = ''
    #pdb.set_trace()
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

def by_rule(request):
    rules = Regulation.objects.all()
    content = {'rules':rules}
    return render(request, 'list_rules.html', content)

def text_rules(request,rules_id):
    current_rule = Regulation.objects.get(pk=rules_id)
    content={'rule':current_rule }
    return render(request,'full_rules.html', content)

