from audioop import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.http import HttpRequest, HttpResponseRedirect
# from django.contrib.auth.forms import UserCreationForm
from authorize.forms import RegisterForm
from Hello_Buddy.views import Profile


def signup(request):
    """Register a new user."""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        # if data can save == true
        if form.is_valid():
            user = form.save()
            profile = Profile(user=user)
            profile.save()
            login(request, user)
            return redirect('home') # redirect is what to go name... page (setting.py)
            # return HttpResponseRedirect(reverse("home"))
    else:
        form = RegisterForm()
    # keep data in each user (dict)
    context = {"form": form}
    return render(request, 'registration/register.html', context)
