from django.db import models
import uuid
from userApi.models import Profile

# Create your models here.
class Message(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    sender = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    recipient = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name="messages")
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    subject = models.CharField(max_length=200, null=True, blank=True)
    body = models.TextField()
    prev_reply_message = models.TextField(null=True, blank=True)
    is_read = models.BooleanField(default=False, null=True)
    is_deleted_by_sender = models.BooleanField(default=False, null=True)
    is_deleted_by_recipient = models.BooleanField(default=False, null=True)
    status = models.CharField(max_length=20, null=False, default="active")
    date_read = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return (f"from: {str(self.sender)}, to: {str(self.recipient)}, subject: {self.subject}, is_read: {self.is_read}, is_deleted by recipient: {self.is_deleted_by_recipient}, is_deleted by sender: {self.is_deleted_by_sender}")
    
    class Meta:
        ordering = ["is_read", "-created"]

class MessageDeleted(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    message = models.OneToOneField(Message, on_delete=models.SET_NULL, null=True, blank=True)
    deleted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return str(self.message)