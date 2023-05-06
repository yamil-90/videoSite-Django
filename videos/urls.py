from django.urls import path
from . import views

app_name = 'videos'

urlpatterns = [
    path('', views.VideosListView.as_view(), name='videos_list'),
]