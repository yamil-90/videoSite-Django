from django.urls import path
from . import views

app_name = 'videos'

urlpatterns = [
    path('', views.VideosListView.as_view(), name='videos_list'),
    path('video/<int:pk>/', views.VideosDetailView.as_view(), name='videos_detail'),
    path('video/create', views.VideoCreateView.as_view(), name='videos_create'),
    path('video/<int:pk>/update', views.VideoUpdateView.as_view(), name='videos_update'),
    path('video/<int:pk>/delete', views.VideoDeleteView.as_view(), name='videos_delete'),
    path('video/<int:pk>/comment', views.CommentCreateView.as_view(), name='videos_comments_create'),
    path('video/<int:pk>/comment/<int:comment_pk>/delete', views.CommentDeleteView.as_view(), name='videos_comments_delete'),

    path('category/<int:pk>/', views.CategoriesDetailView.as_view(), name='videos_category_detail'),
    path('video/<int:pk>/like', views.LikeView.as_view(), name='videos_like'),
    path('video/<int:pk>/dislike', views.DislikeView.as_view(), name='videos_dislike'),

]