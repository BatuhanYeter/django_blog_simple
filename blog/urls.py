from django.urls import path
from . import views
from .views import ( 
    PostListView,
    PostDetailView, 
    PostCreateView, 
    PostUpdateView, 
    PostDeleteView, 
    UserPostListView
)

urlpatterns = [
    # path('', views.home, name='blog-home'), eski hali
    path('', PostListView.as_view(), name='blog-home'), # yeni hali
    path('about/', views.about, name='blog-about'),
    path('post/new/', PostCreateView.as_view(), name='post-create'), 
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'), # pk = primary key
    path('post/<int:pk>/update', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name='post-delete'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'), # <str:username> -> url variable
]

# <app>/<model>_<viewtype>.html