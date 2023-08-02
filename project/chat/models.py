from django.db import models
from users.models import Account
from employers.models import JobPost
# Create your models here.


class Message(models.Model):
    sender = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    postId = models.ForeignKey(JobPost,on_delete=models.CASCADE,related_name='posts',default=None)
    def __str__(self):
        return f"Message from {self.sender.first_name} to {self.recipient.first_name} at {self.created_at}"