from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def get_users(request):
    return HttpResponse("Hello World")

def inicio(request):
    context= {
        "name": "Samuel",
        "email": "kevinsanchezalvarez23@gmail.com",
        "age": 21,
        "resumen":[3,5,67,7,8,8]
    }
    return render(request, "base.html", context=context)