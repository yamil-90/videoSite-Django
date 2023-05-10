from typing import Any, Dict
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Video, Comment, Like
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CommentForm, VideoCreateForm
from django.shortcuts import get_object_or_404, redirect, Http404, render
from django.db.models import Q
from django.core.exceptions import PermissionDenied



class VideosListView(ListView):
    model = Video

    def get_context_data(self, **kwargs: Any):
        strval = self.request.GET.get("search", False)

        query = Q(title__icontains=strval) | Q(description__icontains=strval) if strval else Q()
        
        object_list = Video.objects.filter(query)

        context = super().get_context_data(object_list=object_list, **kwargs)

        return context

class VideosDetailView(DetailView):
    model = Video

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comment_form = CommentForm()
        likes = Like.objects.filter(video=self.object).count()
        if self.request.user.is_authenticated:
            context['liked'] = Like.objects.filter(video=self.object, author=self.request.user).count()
        context['likes'] = likes
        context['comment_list'] = Comment.objects.filter(video=self.object)
        context['comment_form'] = comment_form
        return context

class VideoCreateView(LoginRequiredMixin, CreateView):
    model = Video
    fields = ['title', 'description', 'video_file', 'thumbnail', 'categories']
    success_url = reverse_lazy('videos:videos_list')
    template_name = 'videos/video_form.html'

    def get(self, request, pk=None):
        form = VideoCreateForm()
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def get_success_url(self):
        return reverse_lazy('videos:videos_detail', args=[self.object.id])

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.slug = form.instance.title.replace(" ", "-").lower()
        return super().form_valid(form)

class VideoUpdateView(LoginRequiredMixin, UpdateView):
    model = Video
    fields = ['title', 'description', 'video_file', 'thumbnail']

    def get_success_url(self):
        return reverse_lazy('videos:videos_detail', args=[self.object.id])

    def get_object(self, **kwargs):
        object = super().get_object(**kwargs)
        if object.author != self.request.user:
            raise PermissionDenied("You are not allowed to edit this video.")
        return object

    def form_valid(self, form):
        form.instance.slug = form.instance.title.replace(" ", "-").lower()
        return super().form_valid(form)
    

    

class VideoDeleteView(DeleteView):
    model = Video

class CommentCreateView(LoginRequiredMixin, CreateView):

    def post(self, request, pk):
        video = get_object_or_404(Video, id= pk)
        comment = Comment(text=request.POST['comment'], author=request.user, video=video)
        comment.save()
        return redirect(reverse_lazy('videos:videos_detail', args=[pk]))
    
class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment

    def get_success_url(self):
        return reverse_lazy('videos:videos_detail', args=[self.object.video.id])
    
    def get_object(self, **kwargs):
        object = get_object_or_404(self.get_queryset(), pk=self.kwargs.get('comment_pk'))
        
        # Check if the author of the object is the same as the currently logged in user
       
        if object.author != self.request.user:
            raise Http404("You are not allowed to delete this comment.")
        return object


    
class CategoriesListView(ListView):
    model = Video
    template_name = 'videos/videos_list.html'

    def get_context_data(self, **kwargs: Dict[str, Any]):
        context = super().get_context_data(**kwargs)
        context['object_list'] = Video.objects.filter(category__name=self.kwargs['category'])
        return context
    
class LikeView(LoginRequiredMixin, CreateView):

    def get(self, request, pk):
        return redirect(reverse_lazy('videos:videos_detail', args=[self.kwargs.get('pk')]))

    def get_object(self, **kwargs):
        object = get_object_or_404(self.get_queryset(), pk=self.kwargs.get('pk'))
        
        # Check if the author of the object is the same as the currently logged in user
       
        if object.author != self.request.user:
            raise Http404("You are not allowed to delete this like.")
        return object

    def post(self, request, pk):
        video = get_object_or_404(Video, id= pk)
        like = Like(author=request.user, video=video)
        like.save()
        return redirect(reverse_lazy('videos:videos_detail', args=[pk]))

class DislikeView(LoginRequiredMixin, DeleteView):
    model = Like
    print("hello")

    def get(self):
        return redirect(reverse_lazy('videos:videos_detail', args=[self.object.video.id]))

    def get_success_url(self):
        return reverse_lazy('videos:videos_detail', args=[self.object.video.id])
    
    def get_object(self, **kwargs):
        try:
            object = get_object_or_404(self.get_queryset(), video=self.kwargs.get('pk'), author=self.request.user)
        except:
            raise Http404("You are not allowed to delete this like.")
        
        # Check if the author of the object is the same as the currently logged in user
       
        if object.author != self.request.user:
            raise Http404("You are not allowed to delete this like.")
        return object