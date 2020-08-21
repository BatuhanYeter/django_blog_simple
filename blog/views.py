from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Post
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin # post yaratmak veya update etmek için login şartı koyar
from django.contrib.auth.models import User

# Create your views here.

# dummy data, temporary
# posts = [
#     {
#         'author': 'Batuhan',
#         'title': 'Blog Post 1',
#         'content': 'Keşke uçabilsem',
#         'date_posted': 'August 12, 2020'
#     }
# ]

def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html' # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted'] # yeniden eskiye doğru sıralar
    paginate_by = 5 # pagination, post limit by each page, başlangıçta da 5 tane gösterecek böylece, ilk 5
    # next page -> /?page=2

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html' # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    # spesifik olarak kullanıcıların psotlarını çekmek için
    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(DetailView):
    model = Post
    # <app>/<model>_<viewtype>.html -> post_detail.html dosyası lazım yani

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user # we override the author here
        return super().form_valid(form) # then, olması gerektiği gibi parent classı çalıştırıyor 

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user # we override the author here
        return super().form_valid(form) # then, olması gerektiği gibi parent classı çalıştırıyor

    # update etmeye çalışan kişi post un sahibi mi?    
    def test_func(self): # userpassestextmixin
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    # <app>/<model>_<viewtype>.html -> post_detail.html dosyası lazım yani
    def test_func(self): # userpassestextmixin
            post = self.get_object()
            if self.request.user == post.author:
                return True
            return False
    
    # error msg: No URL to redirect to. Provide a success_url. To fix it:
    success_url = '/'

def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})

