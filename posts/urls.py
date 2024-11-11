from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    
    path('',views.index,name='index' ),
    path('NewPost/',views.New_Post,name='NewPost' ),
    path('<uuid:post_id>/',views.PostDetail,name='PostDetail' ),
    
    
]