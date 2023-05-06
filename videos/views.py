from typing import Any, Dict
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Video, Comment
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CommentForm
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Q

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
        context['comment_list'] = Comment.objects.filter(video=self.object)
        context['comment_form'] = comment_form
        return context

class VideoCreateView(LoginRequiredMixin, CreateView):
    model = Video
    fields = ['title', 'description', 'video_file', 'thumbnail']
    success_url = reverse_lazy('videos:videos_list')

    def get_success_url(self):
        return reverse_lazy('videos:videos_detail', args=[self.object.id])

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.slug = form.instance.title.replace(" ", "-").lower()
        return super().form_valid(form)

class VideoUpdateView(LoginRequiredMixin, UpdateView):
    model = Video
    fields = ['title', 'description', 'url']

    def get_success_url(self):
        return reverse_lazy('videos:videos_detail', args=[self.object.id])

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