from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.http.response import HttpResponse

# Create your views here.

def home(request):
    return render(request, 'Hello_Buddy/home.html')

def aboutus(request):
    return render(request, 'Hello_Buddy/aboutus.html')

def reverse_to_home(self):
    """redirect to homepage"""
    return HttpResponseRedirect(reverse('home'))