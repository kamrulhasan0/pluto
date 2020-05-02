from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import LoginForm,SignUpForm

# Create your views here.

def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "You are account is created successfully!!!")
            return redirect('user:Login')
    else:
        form = SignUpForm()
    context = {'form':form}
    return render(request, 'user/signup.html', context)


def Login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username = username, password = password)
            if user is not None:
                if not user.is_staff:
                    user.is_staff = True
                    user.save()
                login(request, user)
                messages.success(request, 'You are logged in!!!')
                return redirect('main:home')
            else:
                messages.warning(request, 'Invalid Username or Password!!!')
                return redirect('user:Login')
    else:
        form = LoginForm()
    context = {'form':form}
    return render(request, 'user/login.html', context)
