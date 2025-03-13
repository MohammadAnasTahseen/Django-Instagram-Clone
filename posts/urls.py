from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    
    path('index',views.index,name='index' ),
    path('NewPost/',views.New_Post,name='NewPost' ),
    path('<uuid:post_id>/',views.PostDetail,name='PostDetail' ),
    path('<uuid:post_id>/likes',views.PostLike,name='PostLikes' ),
    path('<uuid:post_id>/favourite',views.FavoritePost,name='FavoritePost' ),
    
    
]