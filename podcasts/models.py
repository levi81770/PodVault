from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg


class Podcast(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    host = models.CharField(max_length=200)
    image_url = models.CharField(max_length=500, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('podcast_detail', kwargs={'pk': self.pk})

    def average_rating(self):
        result = self.reviews.aggregate(Avg('rating'))
        return result['rating__avg']    
    
    def review_count(self):
        return self.reviews.count()


class Review(models.Model):
    podcast = models.ForeignKey(Podcast, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.podcast.title} - {self.rating}/5'

    def get_absolute_url(self):
        return self.podcast.get_absolute_url()


class Playlist(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    podcasts = models.ManyToManyField(Podcast, blank=True, related_name='playlists')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('playlist_detail', kwargs={'pk': self.pk})