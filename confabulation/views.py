
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from confabulation.models import User_Message
from django.contrib.auth.models import User
from user_auths.models import UserProfile
from django.db.models import Q
from django.core.paginator import Paginator
from django.db.models import OuterRef, Subquery, Exists

@login_required
@login_required
def inbox(request):
    user = request.user
    messages = User_Message.get_message(user=user)  # ✅ Now handled correctly
    active_direct = None
    directs = None
    profile = get_object_or_404(UserProfile, user=user)

    if messages:
        message = messages[0]
        active_direct = message['user'].username  # ✅ Fixed

        directs = User_Message.objects.filter(
            Q(user=user, reciepient=message['user']) | Q(user=message['user'], reciepient=user)
        ).order_by('date')

        # Mark messages as read
        User_Message.objects.filter(
            sender=message['user'], reciepient=user, is_read=False
        ).update(is_read=True)

        for msg in messages:  # ✅ Use `msg`, since `message` is already defined
            if msg['user'].username == active_direct:
                msg['unread'] = 0  # ✅ Corrected

    context = {
        'directs': directs,
        'messages': messages,
        'active_direct': active_direct,
        'profile': profile,
    }
    return render(request, 'Confabulations/inbox_msg.html', context)




@login_required
def Directs(request, username):
    user = request.user
    messages = User_Message.get_message(user=user)
    active_direct = username

    directs = User_Message.objects.filter(
        Q(user=user, reciepient__username=username) | Q(user__username=username, reciepient=user)
    ).order_by('date').distinct()

    # Mark messages as read
    User_Message.objects.filter(
        sender__username=username, reciepient=user, is_read=False
    ).update(is_read=True)

    for msg in messages:  # ✅ Use `msg` instead of `message`
        if msg['user'].username == username:
            msg['unread'] = 0  # ✅ Corrected

    context = {
        'directs': directs,
        'messages': messages,
        'active_direct': active_direct,
    }
    return render(request, 'Confabulations/inbox_msg.html', context)


def SendDirect(request):
    from_user = request.user
    to_user_username = request.POST.get('to_user')
    body = request.POST.get('body')

    if request.method == "POST":
        to_user = User.objects.get(username=to_user_username)
        User_Message.sender_message(from_user, to_user, body)
        return redirect('message')

def UserSearch(request):
    query = request.GET.get('q')
    context = {}
    if query:
        users = User.objects.filter(Q(username__icontains=query))

        # Paginator
        paginator = Paginator(users, 8)
        page_number = request.GET.get('page')
        users_paginator = paginator.get_page(page_number)

        context = { 
            'users': users_paginator,
            }

    return render(request, 'Confabulations/search.html', context)


# def UserSearch(request):
#     query = request.GET.get('q', '')
#     if query:
#         users = User.objects.filter(Q(username__icontains=query)).values('username', 'userprofile__image', 'userprofile__first_name', 'userprofile__last_name')

#         return JsonResponse({'users': list(users)})

#     return JsonResponse({'users': []})

# def NewConversation(request, username):
#     from_user = request.user
#     body = ''
#     try:
#         to_user = User.objects.get(username=username)
#     except Exception as e:
#         return redirect('search-users')
#     if from_user != to_user:
#         User_Message.sender_message(from_user, to_user, body)
#     return redirect('message')