from django.db import models
from django.contrib.auth.models import User


class Chat(models.Model):
    users = models.ManyToManyField(User, related_name='chats')
    name = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name or str(self.pk)

    def last_10_messages(self):
        return self.messages.order_by('-sent_at').all()[:10]

    def other_user(self, user):
        return self.users.exclude(pk=user.pk).first()

    def get_absolute_url(self):
        return reverse('chat_room', args=[str(self.other_user(request.user).username)])



class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
