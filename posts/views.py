from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from comments.forms import PostCommentsForm
from comments.models import Comment
from posts.models import Likes, Tag, Stream, Follow, Post
from user_auths.models import UserProfile

from django.http import HttpResponseRedirect, JsonResponse

from django.contrib.auth.decorators import login_required
from posts.forms import NewPost
# Create your views here.
def index(request):
    user=request.user
    print(user,"ssssssssssssssssss")
    posts=Stream.objects.filter(stream_user=user.id)
    print("------------",posts)
    group_ids=[]
    for post in posts:
        group_ids.append(post.post_id)

    # posted_items = Post.objects.filter(user=user).order_by('-postedTime')
    posted_items = Post.objects.filter(id__in=group_ids).all().order_by('-postedTime')
    print("Posted Items:", posted_items)
    for post in posted_items:
        
        print("Posted by:", post.user)  # Accessing user attribute for each post
        print("Likes:", post.like)
        print("-------------------------------")
    
    context={
        'post_items':posted_items,
        'user':user
    }
   
    return render(request, 'Post_tempplates/index.html',context)


def New_Post(request):
    user = request.user
    print('-----------',user)
    tags_objs=[]
    if request.method == 'POST':
        form=NewPost(request.POST, request.FILES)
        if form.is_valid():
            picture = form.cleaned_data.get('picture')
            caption=form.cleaned_data.get('caption')
            tag_form=form.cleaned_data.get('tags')
            print(f"------{picture},{caption},{tag_form}------- ")
            tags_list=list(tag_form.split(','))
            print(f"------{tags_list}------- ")
            for tag in tags_list:
                print("insied for")
                t, created = Tag.objects.get_or_create(title=tag)
                tags_objs.append(t)
            p, created = Post.objects.get_or_create(pictures=picture, captions=caption, user=user)
            p.tag.set(tags_objs)
            p.save()
            return redirect('index')
        else:
            print("fornm not valid")
    else:
        form=NewPost()
    context={'form':form}
    return render(request,'Post_tempplates/new_post.html',context)

                                   ########################## for own post and followed users posts ##########################
# def index(request):
#     from django.db.models import Q
#     user = request.user
#     print(f"Current User: {user}")

#     # 🔹 Get all posts from the Stream table where `stream_user` is the current user
#     stream_posts = Stream.objects.filter(stream_user=user)
#     print(f"Stream Posts for {user}: {stream_posts}")

#     # 🔹 Get post IDs from the stream (i.e., posts made by followed users)
#     group_ids = [post.post.id for post in stream_posts]

#     # 🔹 Get posts: 
#     # 1️⃣ Posts from followed users (from Stream table)
#     # 2️⃣ User's own posts
#     posted_items = Post.objects.filter(
#         Q(id__in=group_ids) | Q(user=user)
#     ).order_by('-postedTime')

#     print("Final Posts in Feed:")
#     for post in posted_items:
#         print(f"Post ID: {post.id} | Posted by: {post.user} | Likes: {post.like}")

#     context = {
#         'post_items': posted_items,
#         'user': user
#     }

#     return render(request, 'Post_tempplates/index.html', context)




               ########################## for own post and followed users posts ##########################





def PostDetail(request, post_id):
    user = request.user
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(post=post).order_by('-date')

    if request.method == "POST":
        form = PostCommentsForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = user
            comment.save()
            return HttpResponseRedirect(reverse('PostDetail', args=[post.id]))
    else:
        form = PostCommentsForm()

    context = {
        'post': post,
        'form': form,
        'comments': comments
    }

    return render(request, 'Post_tempplates/post_detail.html', context)


def PostLike(request,post_id):
    user=request.user
    post=Post.objects.get(id=post_id)
    current_post_likes=post.like

    print(f"post:-{post}---------------------current_post_likes:-{current_post_likes}")

    liked=Likes.objects.filter(user=user, Post=post).count()
    if not liked:
        liked = Likes.objects.create(user=user, Post=post)

        current_post_likes=current_post_likes + 1

    else:
        liked=Likes.objects.filter(user=user, Post=post).delete()
        current_post_likes=current_post_likes - 1

    post.like = current_post_likes
    post.save()

    return  HttpResponseRedirect(reverse('PostDetail' , args=[post_id]) )

# def PostLike(request, post_id):
#     if request.method == "POST":
#         user = request.user
#         post = Post.objects.get(id=post_id)
#         liked = Likes.objects.filter(user=user, Post=post).exists()

#         if liked:
#             Likes.objects.filter(user=user, Post=post).delete()
#             post.like -= 1
#             liked = False
#         else:
#             Likes.objects.create(user=user, Post=post)
#             post.like += 1
#             liked = True

#         post.save()

#         # Respond with JSON if it's an AJAX request
#         if request.headers.get('x-requested-with') == 'XMLHttpRequest':
#             return JsonResponse({'liked': liked, 'like_count': post.like})

#         return HttpResponseRedirect(reverse('PostDetail', args=[post_id]))



def FavoritePost(request,post_id):
    user=request.user
    post=Post.objects.get(id=post_id)
    profile=UserProfile.objects.get(user=user)
    if profile.favourite.filter(id=post_id).exists():
        profile.favourite.remove(post)
    else:
        profile.favourite.add(post)
    return  HttpResponseRedirect(reverse('PostDetail' , args=[post_id]) )

   


 

  