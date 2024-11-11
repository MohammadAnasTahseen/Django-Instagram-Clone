from django.shortcuts import get_object_or_404, redirect, render
from posts.models import Tag, Stream, Follow, Post
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
   
    return render(request, 'index.html',context)


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
    return render(request,'new_post.html',context)




def PostDetail(request,post_id):
    post=get_object_or_404(Post,id=post_id)
    context={
        'post':post
    }
    return render(request,'post_detail.html',context)