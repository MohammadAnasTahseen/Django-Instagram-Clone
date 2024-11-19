from urllib import request
from django.urls import resolve
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User
from django.core.paginator import Paginator

from posts.models import Post
from user_auths.models import UserProfile
# Create your views here.
def User_Profile(request,username):  
    user=get_object_or_404(User,username=username)
    profile=UserProfile.objects.get(user=user)
    print("------------------Profile:-----------", profile)
    url_name=resolve(request.path).url_name
    if url_name=='profile': 
          posts=Post.objects.filter(user=user).order_by('-postedTime')

          print("------------------Posts:-----------", posts)

    else:
          posts=profile.favourite.all()


    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page')
    posts_paginator = paginator.get_page(page_number)

    context={
      #   'user':user,
        'profile':profile,
        'posts':posts,
        'posts_paginator':posts_paginator,
        'url_name':url_name
    }
    return render(request,'User_Templates/user_profile.html',context)
