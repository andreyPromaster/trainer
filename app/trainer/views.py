from django.shortcuts import render

# Create your views here.
def index(request):

    # Отрисовка HTML-шаблона index.html с данными внутри 
    # переменной контекста context
    return render(
        request,
        'index.html',
    )
