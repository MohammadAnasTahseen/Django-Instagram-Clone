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

    # def sender_message(from_user, to_user, body):
    #     sender_message = User_Message(
    #         user=from_user,
    #         sender = from_user,
    #         reciepient = to_user,
    #         body = body,
    #         is_read = True
    #         )
    #     sender_message.save()
    
    #     reciepient_message = User_Message(
    #         user=to_user,
    #         sender = from_user,
    #         reciepient = from_user,
    #         body = body,
    #         is_read = True
    #         )
    #     reciepient_message.save()
    #     return sender_message
    
    def sender_message(from_user, to_user, body):
        print("from models sender message called")
        message = User_Message.objects.create(
            user=from_user,
            sender=from_user,
            reciepient=to_user,
            body=body,
            is_read=False  # Message is unread initially
    )
        return message






    @staticmethod
    def get_message(user):
        users = {}
        messages = User_Message.objects.filter(
            Q(sender=user) | Q(reciepient=user)
        ).values('sender', 'reciepient').annotate(last=Max('date')).order_by('-last')

        for message in messages:
            if message['sender'] == user.id:
                other_user_id = message['reciepient']
            else:
                other_user_id = message['sender']

            if other_user_id not in users:  # Prevent duplicate users
                other_user = User.objects.get(pk=other_user_id)
                users[other_user_id] = {
                    'user': other_user,
                    'last': message['last'],
                    'unread': User_Message.objects.filter(
                        sender=other_user, reciepient=user, is_read=False
                    ).count()
                }

        return list(users.values())  # Convert dictionary back to list


            