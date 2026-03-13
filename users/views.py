from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.http import HttpResponse

from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegisterForm
from users.models import Product



# Create your views here.
def get_user(request):
    return HttpResponse("Hello World")

def inicio(request):
    products = Product.objects.all()
    context = {
        "products":products
    }
    return render(request, "base.html",context=context)

def acerca_de(request):
    return render(request, "acerca_de.html")

def list_products(request):
    products = Product.objects.all()
    return render(request, "products.html",context={"products":products})


def register(request):

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('inicio')

    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})

