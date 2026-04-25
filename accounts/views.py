from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserSignupForm

def signup(request):
    if request.method == "POST":
        form = UserSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect("music_list")
    else:
        form = UserSignupForm()
    return render(request, "registration/signup.html", {"form": form})
