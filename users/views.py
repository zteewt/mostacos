from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm

def register_view(request):
    if request.user.is_authenticated:
        return redirect('profile')
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = RegisterForm()
    
    return render(request, 'users/register.html', {
        'form': form,
        'login_url': 'login'
    })

def login_view(request):
    if request.user.is_authenticated:
        return redirect('profile')
    
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = LoginForm()
    
    return render(request, 'users/login.html', {
        'form': form,
        'register_url': 'register'
    })

@login_required
def profile_view(request):
    return render(request, 'users/profile.html', {
        'user': request.user
    })

def logout_view(request):
    logout(request)
    return redirect('login')