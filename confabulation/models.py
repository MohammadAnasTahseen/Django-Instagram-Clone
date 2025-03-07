from django.db import models

# Create your models here.

from django.contrib.auth.models import User
from django.db.models import Max
from django.forms import DateTimeField

from django.db.models import Q


class User_Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="from_user")
    reciepient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="to_user")
    body = models.TextField(null=True)
    date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def sender_message(from_user, to_user, body):
        sender_message = User_Message(
            user=from_user,
            sender = from_user,
            reciepient = to_user,
            body = body,
            is_read = True
            )
        sender_message.save()
    
        reciepient_message = User_Message(
            user=to_user,
            sender = from_user,
            reciepient = from_user,
            body = body,
            is_read = True
            )
        reciepient_message.save()
        return sender_message

    # def get_message(user):
    #     users = []
    #     messages = User_Message.objects.filter(Q(user=user) | Q(reciepient=user)).values('reciepient').annotate(last=Max('date')).order_by('-last')

    #     # messages = User_Message.objects.filter(user=user).values('reciepient').annotate(last=Max('date')).order_by('-last')
    #     for message in messages:
    #         users.append({
    #             'user': User.objects.get(pk=message['reciepient']),
    #             'last': message['last'],
    #             'unread': User_Message.objects.filter(user=user, reciepient__pk=message['reciepient'], is_read=False).count()
    #         })
    #     return users

    @staticmethod
    def get_message(user):
        users = []
        messages = User_Message.objects.filter(
            Q(sender=user) | Q(reciepient=user)  # Track both sent & received messages
        ).values('sender', 'reciepient').annotate(last=Max('date')).order_by('-last')

        for message in messages:
            # Determine the other user in the conversation
            if message['sender'] == user.id:
                other_user = User.objects.get(pk=message['reciepient'])  # User is the sender
            else:
                other_user = User.objects.get(pk=message['sender'])  # User is the recipient
            
            users.append({
                'user': other_user,
                'last': message['last'],
                'unread': User_Message.objects.filter(
                    sender=other_user, reciepient=user, is_read=False  # Count unread messages the user received
                ).count()
            })

        return users


            