from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('podcasts/', views.PodcastList.as_view(), name='podcast_list'),
    path('podcasts/<int:pk>/', views.PodcastDetail.as_view(), name='podcast_detail'),
]