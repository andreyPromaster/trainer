from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login,logout
from .forms import LoginForm
from .forms import RegisterForms, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.contrib import messages
from math import floor


def logout_view(request):
    logout(request)
    return redirect("/trainer")

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST) #create form

        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])  # find user
            if user is not None:
                if user.is_active:
                    login(request, user) #create session
                    return redirect("/trainer/dashboard")#HttpResponse('OK')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'account/login_form.html', {'form': form})
#@login_required
#def dashboard(request):
#    return render(request, 'trainer/dashboard.html', {'section': 'dashboard'})
def register(request):
    if request.method == "POST":

        form = RegisterForms(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Акаўнт створаны ')
            return redirect("/account/login")   
    else:
        form = RegisterForms()

    return render(request, "account/registration/registrator.html", {'form':form})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, 
                                        request.FILES, 
                                        instance=request.user.profile)  # request.FILES is show the selected image or file

        if form.is_valid() and profile_form.is_valid():
            form.save()
            profile_form.save(False)#  it will return an object that hasn’t yet been saved to the database.
            messages.success(request, f'Ваш акаўнт зменены')
            #custom_form.user = user_form
            #custom_form.save()
            return redirect('/account/edit_profile/')
            #return HttpResponse('ok')
    else:
        form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
        args = {}
        args['form'] = form
        args['profile_form'] = profile_form
        exp = ExperienceUser()  
        args['level'] = exp.getlevel(request.user.profile.experience) 
        args['rank'] = exp.getRank(args['level'])
        return render(request, 'account/profile/edit_profile.html', args)

class ExperienceUser:

    def getlevel(self, exp):
        return floor(pow(exp / 100, 7/10)) 

    def getExperience(self, level):
        return round (pow(level, 10/7) * 100)

    def getRank(self, level):
        rank = ""
        if level < 5:
            rank = "Навічок"
        elif level < 15:
            rank = "Карыстальнік"
        elif level < 30:
            rank = "Актыўны"
        elif level < 45:
            rank = "Гігант думак"
        elif level < 60:
            rank = "Старэйшына"
        elif level < 75:
            rank = "Мовазнаўца"
        elif level < 100:
            rank = "Ветэран"
        elif level < 125:
            rank = "Генерал"
        else:
            rank = "Францыск Скарына"
        return rank

