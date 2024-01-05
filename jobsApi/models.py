from django.db import models
from userApi.models import Profile, EmploymentType, Location, Skills
import uuid

# Create your models here.
class Jobs(models.Model):
    user_posted = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    job_title = models.CharField(max_length=100, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    job_detail = models.TextField(max_length=1000, null=True, blank=True)
    experience_level = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=20, default="Open", null=True, blank=True)

    def __str__(self) -> str:
        return self.job_title
    
class JobEmploymentType(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    jobs = models.ForeignKey(Jobs, on_delete=models.CASCADE, null=True, blank=True)
    employment_type  = models.ForeignKey(EmploymentType, on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self) -> str:
        return f"{str(self.jobs.job_title), str(self.employment_type.type)}"

class JobSalaryRates(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    job = models.OneToOneField(Jobs, null=False, blank=False, on_delete=models.CASCADE)
    nominal = models.FloatField(null=False, blank=False)
    paid_period = models.CharField(max_length=20, null=False, blank=False)

    def __str__(self) -> str:
        return str(self.nominal)

class InterestedUsers(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    job = models.ForeignKey(Jobs, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self) -> str:
        return f"{str(self.user)}, {str(self.job)}, {self.status}"

class JobLocation(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    job = models.ForeignKey(Jobs, on_delete=models.CASCADE, null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self) -> str:
        return f"{str(self.job.job_title), str(self.location.location)}"

class JobSkills(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    job = models.ForeignKey(Jobs, on_delete=models.CASCADE, null=True, blank=True)
    skill = models.ForeignKey(Skills, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.job.job_title, self.skill.skill_name}"