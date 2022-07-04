from django.shortcuts import get_object_or_404, render
from django.views import generic, View
from .models import Post
from .forms import CommentForm

class PostList(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status=1).order_by('-created_on') ##Only want published posts to be visible to the user hence status=1
    template_name = 'index.html' # View will render
    paginate_by = 6 ##Limiting the number of posts that are listed on the front page
    
    
class PostDetail(View):
    
    def get(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by("-created_on")
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        return render(
            request,
            "post_detail.html",
            {
                "post": post,
                "comments": comments,
                "liked": liked,
                "comment_form": CommentForm()
            },
        )