from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import RegisterForm


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, '¡Registro exitoso! Bienvenido a tu cuenta.')
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Hay un problema con tu registro. Por favor verifica los datos.')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def home(request):
    return render(request, 'home.html')

