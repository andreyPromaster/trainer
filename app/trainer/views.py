from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import FindWordForm
import pdb
from .dictionary import Parcer

def index(request):
    return render(
        request,
        'index.html',
    )
@login_required (login_url = '/account/login/')
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