
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, DetailView
from .models import Podcast


class Home(LoginView):
    template_name = 'home.html'


class PodcastList(ListView):
    model = Podcast
    template_name = 'podcasts/index.html'
    context_object_name = 'podcasts'


class PodcastDetail(DetailView):
    model = Podcast
    template_name = 'podcasts/detail.html'
    context_object_name = 'podcast'



class LogoutUser(LogoutView):
    next_page = 'home'

def signup(request):
    error_message = ''

    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            error_message = 'Invalid sign up - try again'

    form = UserCreationForm()
    context = {
        'form': form,
        'error_message': error_message
    }

    return render(request, 'signup.html', context)