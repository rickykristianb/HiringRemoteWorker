from django.db import models
from userApi.models import Profile
import uuid

# Create your models here.
class Job(models.Model):
    user_posted = models.OneToOneField(Profile, on_delete=models.CASCADE, null=True, blank=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    job_title = models.CharField(max_length=100, null=False, blank=False)
    job_location = models.CharField(max_length=100, null=False, blank=False)
    job_salary = models.FloatField()
    job_type = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    job_detail = models.TextField(max_length=1000, null=True, blank=True)
    experience_level = models.CharField(max_length=100, null=True, blank=True)
    
    def __str__(self) -> str:
        return self.job_title

class InterestedUser(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self) -> str:
        return f"{str(self.user)}, {str(self.job)}, {self.status}"

class WorkingHistory(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self) -> str:
        return str(self.user)