from django.views.generic import TemplateView, ListView, DetailView
from .models import Podcast


class Home(TemplateView):
    template_name = 'home.html'


class PodcastList(ListView):
    model = Podcast
    template_name = 'podcasts/index.html'
    context_object_name = 'podcasts'


class PodcastDetail(DetailView):
    model = Podcast
    template_name = 'podcasts/detail.html'
    context_object_name = 'podcast'