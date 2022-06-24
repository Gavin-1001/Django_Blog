from django.shortcuts import render
from django.views import generic
from .models import Post

class PostList(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status=1).order_by('-created_by') ##Only want published posts to be visible to the user hence status=1
    template_name = 'index.html' # View will render
    paginate_by: 6 ##Limiting the number of posts that are listed on the front page