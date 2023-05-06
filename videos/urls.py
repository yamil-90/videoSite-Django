from django.urls import path
from . import views

app_name = 'videos'

urlpatterns = [
    path('', views.VideosListView.as_view(), name='videos_list'),
    path('<int:pk>/', views.VideosDetailView.as_view(), name='videos_detail'),
    path('video/create', views.VideoCreateView.as_view(), name='videos_create'),
    path('video/<int:pk>/update', views.VideoUpdateView.as_view(), name='videos_update'),
    path('video/<int:pk>/delete', views.VideoDeleteView.as_view(), name='videos_delete'),
    path('video/<int:pk>/comment', views.CommentCreateView.as_view(), name='videos_comments_create'),

]