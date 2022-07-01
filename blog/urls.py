from . import views
from django.urls import path
urlpatterns = [
    path('', views.PostList.as_view(), name="home"),
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    ##1st slug is a path converter, converts text into slug field
    # 2ndthe second slug is just a keyword name parameter "slug"
]