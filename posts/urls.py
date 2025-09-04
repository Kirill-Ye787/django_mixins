from django.urls import path
from . import views
app_name = 'posts'
urlpatterns = [
    path('', views.PostListView.as_view(), name='list'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='detail'),
    path('post/create/', views.PostCreateView.as_view(), name='create'),
    path('post/<int:pk>/edit/', views.PostUpdateView.as_view(), name='edit'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='delete'),
]
