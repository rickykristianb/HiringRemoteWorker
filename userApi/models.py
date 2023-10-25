from django.db import models
from django.contrib.auth.models import User
from django.db.models.functions import Cast
from django.db.models import Sum
from django.db import connection
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
    skills = models.ManyToManyField("Skills", blank=True)
    languages = models.ManyToManyField("Language", blank=True)
    employment_type = models.CharField(max_length=50, null=True, blank=True)
    user_type = models.CharField(max_length=20, null=True, blank=True)
    rate_total = models.FloatField(default=0, null=True, blank=True)
    rate_ratio = models.FloatField(default=0, null=True, blank=True)

    def __str__(self) -> str:
        return self.username
    

class UserRate(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    from_user = models.ForeignKey(Profile, related_name="given_rating", null=True, on_delete=models.CASCADE)
    to_user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    rate_value = models.IntegerField(default=5)

    def __str__(self) -> str:
        return f"{self.from_user}, {self.to_user}" 
    
    class Meta:
        unique_together = ["from_user", "to_user"]
    
    
class Language(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    language = models.CharField(max_length=20, null=True, blank=True)
    proficiency = models.CharField(max_length=20, null=True, blank=True)
    
    def __str__(self) -> str:
        return f"{self.language}, {self.proficiency}"
    

class Skills(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    skill_name = models.CharField(max_length=20, null=True, blank=True)
    skill_level = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.skill_name}, {self.skill_level}"
    
    
class Education(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    user = models.ForeignKey(Profile, null=False, blank=False, default="Personal", on_delete=models.CASCADE)
    major = models.CharField(max_length=50, null=True, blank=True)
    degrees = models.CharField(max_length=20, null=True, blank=True)
    school_name = models.CharField(max_length=100, null=True, blank=True)
    start_year = models.DateField()
    end_year = models.DateField()

    def __str__(self) -> str:
        return f"{self.user}, {self.major}, {self.degrees}"
    
class ExpectedSalary(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user = models.OneToOneField(Profile, null=False, blank=False, default="Personal", on_delete=models.CASCADE)
    currency = models.CharField(max_length=3, null=True, blank=True)
    nominal = models.FloatField()
    paid_period = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self) -> str:
        return str(self.nominal)
    
class Experience(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user = models.ForeignKey(Profile, null=False, blank=False, on_delete=models.CASCADE)
    job_name = models.CharField(max_length=100, null=False, blank=False)
    company_name = models.CharField(max_length=100, null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    details = models.TextField(max_length=600, null=True, blank=True)
    total_exp = models.FloatField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.user}, {self.company_name}, {self.start_date}, {self.end_date}"
    
    
class Networking(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user = models.ForeignKey(Profile, null=False, blank=False, default="Personal", on_delete=models.CASCADE)
    networking_link = models.CharField(max_length=100, null=False, blank=False)
    networking_name = models.CharField(max_length=20, null=True, blank=True)


    def __str__(self) -> str:
        return f"{self.user}, {self.networking_name}, {self.networking_link}"
    
    class Meta:
        unique_together = ["user", "networking_name"]
    
class Portfolio(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user = models.ForeignKey(Profile, null=False, blank=False, default="Personal", on_delete=models.CASCADE)
    portfolio_link = models.CharField(max_length=100, null=False, blank=False)
    portfolio_name = models.CharField(max_length=20, null=True, blank=True)

    @property
    def get_portfolio_name(self):
        return dict(self.PORTFOLIO_CHOICES).get(self.portfolio_name)

    def __str__(self) -> str:
        return f"{self.user}, {self.get_portfolio_name}"
    
    class Meta:
        unique_together = ["user", "portfolio_name"]

class Message(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    sender = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    recipient = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name="messages")
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    subject = models.CharField(max_length=200, null=True, blank=True)
    body = models.TextField()
    is_read = models.BooleanField(default=False, null=True)
    date_read = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return str(self.sender)
    
    class Meta:
        unique_together = ["sender", "recipient"]
        ordering = ["is_read", "-created"]
