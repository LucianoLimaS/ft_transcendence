from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.users.models import Users
from django.utils import timezone
from django.db.models.functions import Now

# class ChatGroup(models.Model):
#     group_name = models.CharField(max_length=128, unique=True)
    
#     def __str__(self):
#         return self.group_name
    
# class GroupMessage(models.Model):
#     group = models.ForeignKey(ChatGroup, related_name='chat_messages', on_delete=models.CASCADE)
#     author = models.ForeignKey(Users, on_delete=models.CASCADE)
#     body = models.CharField(max_length=300)
#     created = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f'{self.author.username} : {self.body}'
    
#     class Meta:
#         ordering = ['-created']

class Chat(models.Model):
    """ user1 = models.ForeignKey(Users, related_name='chats_as_user1', on_delete=models.DO_NOTHING, default=0)
    user2 = models.ForeignKey(Users, related_name='chats_as_user2', on_delete=models.DO_NOTHING, default=0) """
    users = models.ManyToManyField('users.Users', through='ChatUser')
    start_time = models.DateTimeField(db_default=Now())

    def __str__(self):
        return f"Chat between {self.user1.nickname} and {self.user2.nickname}"
    
class ChatUser(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    user = models.ForeignKey('users.Users', on_delete=models.CASCADE)
    joined_at = models.DateTimeField(db_default=Now())

    def __str__(self):
        return f"{self.user.nickname} in chat {self.chat.id}"
    
class Message(models.Model):
    chat = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(Users, related_name='sent_messages', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(db_default=Now())
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.sender.nickname} at {self.timestamp}"