from xml.etree.ElementTree import Comment
from django.shortcuts import get_object_or_404, render, reverse
from django.views import generic, View
from .models import Post
from .forms import CommentForm
from django.http import HttpResponseRedirect

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
                "commented": False, ## tells the user the comment has not been approved
                "liked": liked,
                "comment_form": CommentForm()
            },
        )
        
        
    def post(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by("-created_on")
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True
            
        comment_form = CommentForm(data=request.POST) #variable gets data from form
        
        if(comment_form.is_valid):
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
        else:
            comment_form = CommentForm()
        
        #pseudo code
        #if the commment data in the form is valid(i.e all the fields are inputted) then the email,username will be retrieved from the data and set to the username and user. The comment can be posted and is saved in place
        ## else, if something went wrong with retrieving the data then the form will return an empty comment 
        

        return render(
            request,
            "post_detail.html",
            {
                "post": post,
                "comments": comments,
                "commented": True, ## tells the user that the comment has been approved and allows others to see it 
                "liked": liked,
                "comment_form": CommentForm()
            },
        )
class PostLike(View):
    
    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug) ##gets post
        
        #checks if post has already been liked
        if(post.likes.filter(id=request.user.id).exists()):
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
        
        return HttpResponseRedirect(reverse('post_detail', args=[slug]))
                
            