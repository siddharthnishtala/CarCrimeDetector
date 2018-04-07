from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib import messages


class LandingPage(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'landing.html', context=None)

    def post(self, request, **kwargs):
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('HomePage')
        else:
            messages.error(request, "Login unsuccessful!")
            return render(request, 'landing.html', context=None)


class HomePage(TemplateView):
    def get(self, request, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "Please sign up or login!")
            return render(request, 'landing.html', context=None)
        else:
            return render(request, 'home.html', context={"user": request.user})

class LocBasedHomePage(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'LocBasedHome.html', context=None)