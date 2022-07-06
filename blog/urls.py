from . import views
from django.urls import path
urlpatterns = [
    path('', views.PostList.as_view(), name="home"),
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('like/<slug:slug>', views.PostLike.as_view(), name='post_like'),
    
    ##1st slug is a path converter, converts text into slug field
    # 2nd the second slug is just a keyword name parameter "slug"
    #3rd Is the url for the number of likes on a post
]