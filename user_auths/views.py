from urllib import request
from django.http import HttpResponseRedirect
from django.urls import resolve, reverse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User
from django.core.paginator import Paginator

from posts.models import Follow, Post, Stream
from user_auths.models import UserProfile

from django.db import transaction
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
          print("------------------favourite Posts:-----------", posts)


    paginator = Paginator(posts, 1)
    page_number = request.GET.get('page')
    posts_paginator = paginator.get_page(page_number)


    posts_count = Post.objects.filter(user=user).count()
    following_count = Follow.objects.filter(follower=user).count()
    followers_count = Follow.objects.filter(following=user).count()
    # count_comment = Comment.objects.filter(post=posts).count()
    follow_status = Follow.objects.filter(following=user, follower=request.user).exists()

    context={
      #   'user':user,
        'profile':profile,
        'posts':posts,
        'posts_paginator':posts_paginator,
        'url_name':url_name,
        'posts_count':posts_count,
        'following_count':following_count,
        'followers_count':followers_count,
        'follow_status':follow_status,
    }
    print("------------------Context:-----------", context)
    return render(request,'User_Templates/user_profile.html',context)






def follow_user(request, username, option):
    user = request.user
    following = get_object_or_404(User, username=username)

    try:
        if int(option) == 0:  # Unfollow
            Follow.objects.filter(follower=user, following=following).delete()  # ✅ FIXED: Delete safely
            Stream.objects.filter(stream_user=user, stream_following=following).delete()
        
        else:  # Follow
            f, created = Follow.objects.get_or_create(follower=user, following=following)
            
            if created:
                posts = Post.objects.filter(user=following)[:10]
                
                with transaction.atomic():
                    for post in posts:
                        stream = Stream(post=post, stream_user=user, date=post.postedTime, stream_following=following)
                        stream.save()

        # ✅ Always return an HttpResponseRedirect after any action
        return HttpResponseRedirect(reverse('profile', args=[username]))

    except User.DoesNotExist:
        return HttpResponseRedirect(reverse('profile', args=[username]))


