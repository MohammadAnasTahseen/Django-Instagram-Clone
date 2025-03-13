from urllib import request
from django.http import HttpResponseRedirect
from django.urls import resolve, reverse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.core.paginator import Paginator

from posts.models import Follow, Post, Stream
from user_auths.forms import EditProfileForm, UserLoginForm, UserRegisterForm
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




def edit_profile(request):
    
    print("------------------Edit Profile:-----------")
    
    user=request.user.id
    profile = UserProfile.objects.get(user__id=user)
    # print("------------------Profile:-----------", profile.first_name)

    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile.picture = form.cleaned_data.get('picture')
            profile.first_name = form.cleaned_data.get('first_name')
            profile.last_name = form.cleaned_data.get('last_name')
            profile.bio = form.cleaned_data.get('bio')
            profile.url = form.cleaned_data.get('url')
            profile.location = form.cleaned_data.get('location')

            profile.save() 

            return HttpResponseRedirect(reverse('profile', args=[profile.user.username]))
    else:
        form = EditProfileForm(instance=profile)
        context={
            'form':form,
            
            }
    return render(request,'User_Templates/edit_profile.html',context)


     
from django.contrib import messages
from django.contrib.auth import authenticate, login

def register(request):
    print("------------------Register:-----------")
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        print("------------------Form:-----------", form)
        if form.is_valid():
            print("##########################form is valid")
            form.save()  # Just save the user, don't log them in
            messages.success(request, "Your account has been created! Please log in.")
            return redirect('login')  # Redirect to login page after successful registration
        else:
            messages.error(request, "There was an error. Please try again.")
    else:
        form = UserRegisterForm()

    return render(request, 'Auth_Templates/sign_up.html', {'form': form})


def login_view(request):
    print(f"---- Request Method: {request.method} ----")
    
    if request.method == 'POST':
        print(f"POST Data: {request.POST}")  # Debugging
        
        form = UserLoginForm(request,request.POST)
        if form.is_valid():
            print("Form is valid")
            
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            print(f"Username: {username}, Password: {password}")
            
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                print("User logged in successfully")
                return redirect('index')
            else:
                print("Invalid username or password")
                form.add_error(None, "Invalid username or password")
        else:
            print("Form is NOT valid")
            print(form.errors)  # Print form errors for debugging

    else:
        form = UserLoginForm()
    
    return render(request, 'Auth_Templates/login.html', {'form': form})
