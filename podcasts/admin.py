from django.contrib import admin
from .models import Podcast, Review, Playlist


admin.site.register(Podcast)
admin.site.register(Review)
admin.site.register(Playlist)