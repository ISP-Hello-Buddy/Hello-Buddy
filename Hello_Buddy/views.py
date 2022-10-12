from django.shortcuts import render
from django.http.response import HttpResponse

# Create your views here.

def home(request):
    return render(request, 'Hello_Buddy/home.html')
