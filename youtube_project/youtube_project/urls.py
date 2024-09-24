from django.urls import path
from youtube_app import views

urlpatterns = [
    path('get_top_videos/', views.get_top_videos, name='get_top_videos'),
]
