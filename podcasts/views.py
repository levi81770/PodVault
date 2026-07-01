
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
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

class PodcastCreate(LoginRequiredMixin, CreateView):
    model = Podcast
    fields = ['title', 'description', 'host', 'image_url']
    template_name = 'podcasts/form.html'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class PodcastUpdate(LoginRequiredMixin, UpdateView):
    model = Podcast
    fields = ['title', 'description', 'host', 'image_url']
    template_name = 'podcasts/form.html'

class PodcastDelete(LoginRequiredMixin, DeleteView):
    model = Podcast
    success_url = reverse_lazy('podcast_list')

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