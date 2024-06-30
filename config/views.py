from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import auth
from django.views import View

def home(request):
    context = {}
    if request.user.is_authenticated:
        context['userStatus'] = 'zalogowany'
    else:
        context['userStatus'] = 'niezalogowany'
    return render(request, 'django_app/home.html', context)

def signup_page(request):
    context = {}
    if request.method == 'POST':
        try:
            user = User.objects.get(username=request.POST['username'])
            context['error'] = 'Podana nazwa użytkownika już istnieje! Proszę podać inną nazwę użytkownika.'
            return render(request, 'django_app/signup.html', context)
        except User.DoesNotExist:
            if request.POST['password1'] != request.POST['password2']:
                context['error'] = 'Podane hasła nie są takie same! Proszę wprowadzić identyczne hasła.'
                return render(request, 'django_app/signup.html', context)
            else:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                auth.login(request, user)
                return redirect('home')
    else:
        return render(request, 'django_app/signup.html', context)


def login_page(request): 
    context = {}
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            context['error'] = 'Podane hasło lub login są błędne! Podaj poprawne dane.'
            return render(request, 'django_app/login.html', context)
    else:
        return render(request, 'django_app/login.html')
    
def logout_page(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('home')

def public_page(request):
    return render(request, 'django_app/publicpage.html')

@login_required
def private_page(request):
    return render(request, 'django_app/privatepage.html')

class PrivateClass_page(View):
    def get(self, request):
        return render(request, 'django_app/privateclasspage.html')