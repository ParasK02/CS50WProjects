
from django.urls import path

from . import views

urlpatterns = [

    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("following",views.get_following, name="followingPosts"),
    path("user/<str:username>",views.get_user_info, name="getUser"),

    
    #API Routes 
    path("posts",views.newPost, name="newPost"),
    path("posts/<int:post_id>", views.post, name="post"),
    path("posts/<str:post_type>", views.get_posts, name="getPosts"),
    path("posts/edit/<int:post_id>", views.editPost,name="editPost"),
    path("users/<int:user_id>", views.getUser, name='followUser'),
    path("liked_posts", views.liked_posts, name="liked_posts"),
    

    

]
