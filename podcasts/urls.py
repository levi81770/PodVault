from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('logout/', views.LogoutUser.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('podcasts/', views.PodcastList.as_view(), name='podcast_list'),
    path('podcasts/create/', views.PodcastCreate.as_view(), name='podcast_create'),
    path('podcasts/<int:pk>/', views.PodcastDetail.as_view(), name='podcast_detail'),
    path('podcasts/<int:pk>/update/', views.PodcastUpdate.as_view(), name='podcast_update'),
    path('podcasts/<int:pk>/delete/', views.PodcastDelete.as_view(), name='podcast_delete'),
    path('podcasts/<int:pk>/reviews/create/', views.ReviewCreate.as_view(), name='review_create'),
    path('reviews/<int:pk>/update/', views.ReviewUpdate.as_view(), name='review_update'),
    path('reviews/<int:pk>/delete/', views.ReviewDelete.as_view(), name='review_delete'),
]