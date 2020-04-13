from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login,logout
from .forms import LoginForm
from .forms import RegisterForms, EditProfileForm, ProfileForm
from django.contrib.auth.decorators import login_required
from datetime import datetime

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
        return redirect("/account/login")   
    else:
        form = RegisterForms()

    return render(request, "account/registration/registrator.html", {'form':form})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)  # request.FILES is show the selected image or file

        if form.is_valid() and profile_form.is_valid():
            user_form = form.save()
            custom_form = profile_form.save(False)# then it will return an object that hasn’t yet been saved to the database.
            custom_form.user = user_form
            custom_form.save()
            #return redirect('accounts:view_profile')
            return HttpResponse('ok')
    else:
        form = EditProfileForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
        args = {}
        args['form'] = form
        args['profile_form'] = profile_form
        return render(request, 'account/profile/edit_profile.html', args)


