from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.
class Profile(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255, null=False, blank=False)
    username = models.CharField(max_length=255, unique=True, null=False, blank=False)
    email = models.EmailField(max_length=255, unique=True, null=False, blank=False)
    location = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=14, unique=True, null=True, blank=True)
    short_intro = models.CharField(max_length=255, null=True, blank=True)
    bio = models.TextField(max_length=1000, null=True, blank=True)
    profile_picture = models.ImageField(null=True, upload_to="profile/", default="profile/user-default.png")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
        # skill_id integer
        # employement_type_id integer
    # user_rate_id integer
    # user_type_id integer
    # experience_id integer
    # education_id integer
    # portofolio_id integer
    # expected_salary_id integer
    # networking_id integer
    # working_history_id integer
    # job_posted_id integer

    def __str__(self) -> str:
        return self.username
    
class Language(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=False)
    LANGUAGE_CHOICES = [
        ("ID", "INDONESIA"),
        ("EN", "ENGLISH"),
    ]
    language = models.CharField(max_length=2, default="ID", choices=LANGUAGE_CHOICES)
    PROFICIENCY_CHOICES = [
        (1, "Native"),
        (2, "Expert"),
        (3, "Fluent"),
        (4, "Intermediate"),
        (5, "Beginner")
    ]
    proficiency = models.IntegerField(choices=PROFICIENCY_CHOICES, default=1)
    
    
    def __str__(self) -> str:
        return f"{self.language}, {self.user}, {self.proficiency}"
    
    class Meta:
        unique_together = ["user", "language"]
    

class Skills(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    skill_name = models.CharField(max_length=20, null=True, blank=True)
    SKILL_LEVEL_CHOICES = [
        (1, "Novice"), 
        (2, "Beginner"), 
        (3, "Advanced Beginner"),
        (4, "Competent"),
        (5, "Proficient"),
        (6, "Expert")
    ]
    skill_level = models.IntegerField(choices=SKILL_LEVEL_CHOICES, default=1)

    def get_skill_level_name(self):
        return dict(self.SKILL_LEVEL_CHOICES).get(self.skill_level)

    def __str__(self) -> str:
        return f"{self.user}, {self.skill_name}, {self.get_skill_level_name()}"
    
    
class EmploymentType(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=False)
    TYPE_CHOICES = [
        (1, "Full-time/Contract"),
        (2, "Full-time/Permanent")
    ]
    type_name = models.IntegerField(choices=TYPE_CHOICES, default=1)

    def get_type_name(self):
        return dict(self.TYPE_CHOICES).get(int(self.type_name))

    def __str__(self) -> str:
        return f"{self.user}, {self.get_type_name()}, {self.type_name}"
    
    class Meta:
        unique_together = ["user", "type_name"]

class UserRate(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    user = models.ForeignKey(User, related_name="rating_owner", null=True, on_delete=models.SET_NULL)
    rated_user = models.ForeignKey(User, related_name='ratings_received', null=True, on_delete=models.SET_NULL)
    rate_total = models.IntegerField(default=0, null=True, blank=True)
    rate_ratio = models.FloatField(default=0, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.user}, {self.rated_user}, {self.rate_total}" 
    
class UserType(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    user = models.OneToOneField(User, null=False, blank=False, default="Personal", on_delete=models.CASCADE)
    TYPE_CHOICES = [
        (1, "Personal"),
        (2, "Company")
    ]
    type_name = models.IntegerField(choices=TYPE_CHOICES, default=1)

    def __str__(self) -> str:
        return f"{self.user}, {str(self.type_name)}"