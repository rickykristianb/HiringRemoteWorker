from django.db import models
from userApi.models import Profile
import uuid

# Create your models here.
class JobPosted(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    user = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    job_title = models.CharField(max_length=50, null=False, blank=False)

    OPEN = "open"
    CLOSE = "close"
    STATUS_CHOICES = [
        (OPEN, "Open"),
        (CLOSE,  "Close")
    ]
    job_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=CLOSE)
    job_location = models.CharField(max_length=50, null=True, blank=True)
    job_salary = models.FloatField()

    FULL_TIME_CONTRACT = "fulltime_contract"
    FULL_TIME_PERMANENT = "fulltime_permanent"
    PART_TIME_CONTRACT = "parttime_contract"
    PART_TIME_PERMANENT = "parttime_permanent"
    TYPE_CHOICES = [
        (FULL_TIME_CONTRACT, "Full-time/Contract"),
        (FULL_TIME_PERMANENT, "Full-time/Permanent"),
        (PART_TIME_CONTRACT, "Part-time/Contract"),
        (PART_TIME_PERMANENT, "Part-time/Permanent")
    ]
    job_type = models.CharField(max_length=50, choices=TYPE_CHOICES, default=FULL_TIME_PERMANENT)
    created_at = models.DateTimeField(auto_now_add=True)
    job_detail = models.TextField(max_length=500)

    ENTRY_LEVEL = "entry_level"
    JUNIOR_LEVEL = "junior_level"
    INTERMEDIATE = "intermediate"
    MIDDLE_LEVEL = "middle"
    SENIOR_LEVEL = "senior"
    
    LEVEL_CHOICES = [
        (ENTRY_LEVEL, "Entry Level"),
        (JUNIOR_LEVEL, "Junior Level"),
        (INTERMEDIATE, "Intermediate"),
        (MIDDLE_LEVEL, "Middle Level"),
        (SENIOR_LEVEL, "Senior Level")
    ]
    experience_level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default=ENTRY_LEVEL)

class JobInterested(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    job = models.ForeignKey(JobPosted, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
