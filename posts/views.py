from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post
from .forms import PostForm
from .mixins import (
    TitleContextMixin, PaginationMixin, CachePageMixin,
    StaffRequiredMixin, OwnerRequiredMixin, SuccessMessageMixin
)
class PostListView(PaginationMixin, CachePageMixin, TitleContextMixin, ListView):
    model = Post
    template_name = 'posts/post_list.html'
    context_object_name = 'posts'
    page_title = 'Посты'
    paginate_by = 5
    cache_timeout = 10
class PostDetailView(TitleContextMixin, DetailView):
    model = Post
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'
    page_title = 'Детали поста'
class PostCreateView(LoginRequiredMixin, StaffRequiredMixin, SuccessMessageMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/post_form.html'
    success_url = reverse_lazy('posts:list')
    success_message = 'Пост создан.'
class PostUpdateView(LoginRequiredMixin, OwnerRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/post_form.html'
    success_url = reverse_lazy('posts:list')
    success_message = 'Пост обновлён.'
class PostDeleteView(LoginRequiredMixin, OwnerRequiredMixin, DeleteView):
    model = Post
    template_name = 'posts/post_confirm_delete.html'
    success_url = reverse_lazy('posts:list')
