from django.shortcuts import render
from django.views.generic import ListView
from .models import Video

class VideosListView(ListView):
    template_name = 'videos/videos_list.html'
    model = Video
