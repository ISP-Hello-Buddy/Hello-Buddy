from django.shortcuts import render
# from django.http.response import HttpResponse
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

def home(request):
    return render(request, 'Hello_Buddy/home.html')
