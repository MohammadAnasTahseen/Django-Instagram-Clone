from urllib import request
from django.urls import resolve
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User
from django.core.paginator import Paginator

from posts.models import Post
from user_auths.models import UserProfile
# Create your views here.
def User_rofile(request,username):  
    user=get_object_or_404(User,username=username)
    profile=UserProfile.objects.get(user=user)
    url_name=resolve(request.path).url_name
    if url_name=='profile': 
          posts=Post.objects.filter(user=user).order_by('-postedTime')

          print("------------------Posts:-----------", posts)

    else:
          posts=UserProfile.favourite.all()


    paginator = Paginator(Post, 8)
    page_number = request.GET.get('page')
    posts_paginator = paginator.get_page(page_number)
