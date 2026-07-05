from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Podcast, Review, Playlist
from django.contrib.auth.decorators import login_required


class Home(LoginView):
    template_name = "home.html"


class PodcastList(ListView):
    model = Podcast
    template_name = "podcasts/index.html"
    context_object_name = "podcasts"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            context["playlists"] = Playlist.objects.filter(owner=self.request.user)

        return context


class PodcastDetail(DetailView):
    model = Podcast
    template_name = "podcasts/detail.html"
    context_object_name = "podcast"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            context["playlists"] = Playlist.objects.filter(owner=self.request.user)

        return context


class PodcastCreate(LoginRequiredMixin, CreateView):
    model = Podcast
    fields = ["title", "description", "host", "image_url"]
    template_name = "podcasts/form.html"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class PodcastUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Podcast
    fields = ["title", "description", "host", "image_url"]
    template_name = "podcasts/form.html"

    def test_func(self):
        return self.get_object().created_by == self.request.user


class PodcastDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Podcast
    success_url = reverse_lazy("podcast_list")

    def test_func(self):
        return self.get_object().created_by == self.request.user


class ReviewCreate(LoginRequiredMixin, CreateView):
    model = Review
    fields = ["rating", "comment"]
    template_name = "podcasts/review_form.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.podcast_id = self.kwargs["pk"]
        return super().form_valid(form)


class ReviewUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Review
    fields = ["rating", "comment"]
    template_name = "podcasts/review_form.html"

    def test_func(self):
        return self.get_object().user == self.request.user


class ReviewDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Review
    template_name = "podcasts/review_confirm_delete.html"

    def test_func(self):
        return self.get_object().user == self.request.user

    def get_success_url(self):
        return self.object.podcast.get_absolute_url()


class PlaylistList(LoginRequiredMixin, ListView):
    model = Playlist
    template_name = "podcasts/playlist_index.html"
    context_object_name = "playlists"

    def get_queryset(self):
        return Playlist.objects.filter(owner=self.request.user)


class PlaylistDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Playlist
    template_name = "podcasts/playlist_detail.html"
    context_object_name = "playlist"

    def test_func(self):
        return self.get_object().owner == self.request.user


class PlaylistCreate(LoginRequiredMixin, CreateView):
    model = Playlist
    fields = ["name", "description"]
    template_name = "podcasts/playlist_form.html"

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class PlaylistUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Playlist
    fields = ["name", "description"]
    template_name = "podcasts/playlist_form.html"

    def test_func(self):
        playlist = self.get_object()
        return playlist.owner == self.request.user


class PlaylistDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Playlist
    template_name = "podcasts/playlist_confirm_delete.html"
    success_url = reverse_lazy("playlist_list")

    def test_func(self):
        playlist = self.get_object()
        return playlist.owner == self.request.user


@login_required
def add_to_playlist(request, podcast_id):
    if request.method == "POST":
        podcast = get_object_or_404(Podcast, id=podcast_id)
        playlist_id = request.POST.get("playlist_id")
        playlist = get_object_or_404(Playlist, id=playlist_id, owner=request.user)

    playlist.podcasts.add(podcast)

    next_url = request.POST.get("next")
    if next_url:
        return redirect(next_url)

    return redirect("podcast_list")


@login_required
def remove_from_playlist(request, playlist_id, podcast_id):
    playlist = get_object_or_404(Playlist, id=playlist_id, owner=request.user)

    podcast = get_object_or_404(Podcast, id=podcast_id)

    if request.method == "POST":
        playlist.podcasts.remove(podcast)

    return redirect("playlist_detail", pk=playlist.id)


class LogoutUser(LogoutView):
    next_page = "home"


def signup(request):
    error_message = ""

    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
        else:
            error_message = "Invalid sign up - try again"

    form = UserCreationForm()
    context = {"form": form, "error_message": error_message}

    return render(request, "signup.html", context)
