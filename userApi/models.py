from django.db import models
# from django.contrib.auth.models import User
from django.conf import settings
# from jobApi.models import JobPosted
import uuid
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin, BaseUserManager  # Custom user

from django.conf import settings
User = settings.AUTH_USER_MODEL    # add to the relation of the user

# Setting User Custom Model
class UserAccountManager(BaseUserManager):
    def create_user(self, email, name, user_type, username, password=None, **kwargs):
        if not email:
            raise ValueError("Users must have an email address")
        
        email = self.normalize_email(email)
        user = self.model(email=email, name=name)
        user.username=username
        user.user_type=user_type
        user.set_password(password)
        user.is_active = True
        user.save()

        return user

    def create_superuser(self, email, name, password=None, **kwargs):
        user = self.create_user(email=email, name=name, password=password)
        user.is_superuser = True
        user.save()
        
        return user

# Setting User Custom Model
class UserAccount(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True, null=False, blank=False)
    name = models.CharField(max_length=255, null=False, blank=False)
    username = models.CharField(max_length=255, unique=True, null=True, blank=True)
    # You can add more fields here
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    user_type = models.CharField(max_length=20, null=True, blank=True)

    objects = UserAccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "username"]  # You can add more field as required fields

    def __str__(self) -> str:
        return self.email

# Create your models here.
class Profile(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255, null=False, blank=False)
    username = models.CharField(max_length=255, unique=True, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True, unique=True)
    phone_number = models.CharField(max_length=14, unique=True, null=True, blank=True)
    short_intro = models.CharField(max_length=255, null=True, blank=True)
    bio = models.TextField(max_length=1000, null=True, blank=True)
    profile_picture = models.ImageField(null=True, upload_to="profile/", default="profile/user-default.png")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    rate_total = models.FloatField(default=0, null=True, blank=True)
    rate_ratio = models.FloatField(default=0, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.email}"
    
    @property
    def get_profile_picture(self):
        if self.profile_picture and hasattr(self.profile_picture, 'url'):
         return f"http://localhost:8000/{self.profile_picture.url}"

class Location(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    location = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.location}, id: {self.id}"


class UserLocation(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    user = models.OneToOneField(Profile, on_delete=models.CASCADE, null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.user}, {self.location}"
    

class EmploymentType(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    type = models.CharField(max_length=20, null=False, blank=False)

    def __str__(self) -> str:
        return f"{self.id},{self.type}"
    

class UserEmploymentType(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=False, blank=False)
    employment_type  = models.ForeignKey(EmploymentType, on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self) -> str:
        return f"{self.user}, {self.employment_type}"
    
    class Meta:
        unique_together = ["user", "employment_type"]


class UserRate(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    from_user = models.ForeignKey(Profile, related_name="given_rating", null=True, on_delete=models.CASCADE)
    to_user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    comment = models.TextField(max_length=1000, null=False, blank=False, default="N/A")
    rate_value = models.IntegerField(default=5)

    def __str__(self) -> str:
        return f"{self.from_user}, {self.to_user}" 
    
    class Meta:
        unique_together = ["from_user", "to_user"]
    
    
class Language(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    user = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.CASCADE)
    language = models.CharField(max_length=20, null=True, blank=True)
    proficiency = models.CharField(max_length=20, null=True, blank=True)
    
    def __str__(self) -> str:
        return f"{self.language}, {self.proficiency}"
    
    class Meta:
        unique_together = ["user", "language"]
    

class Skills(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    skill_name = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.skill_name}"

    
class SkillLevel(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    skill_level = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self) -> str:
        return self.skill_level
    

class UserSkillLevel(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    skills = models.ForeignKey(Skills, on_delete=models.CASCADE)
    skill_level = models.ForeignKey(SkillLevel, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.user}, {self.skills}, {self.skill_level}"
    
    class Meta:
        unique_together = ["user", "skills"]
    
    
class Education(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    user = models.ForeignKey(Profile, null=False, blank=False, default="Personal", on_delete=models.CASCADE)
    major = models.CharField(max_length=50, null=True, blank=True)
    degree = models.CharField(max_length=20, null=True, blank=True)
    school_name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.user}, {self.major}, {self.degree}"
    

class ExpectedSalary(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user = models.OneToOneField(Profile, null=False, blank=False, default="Personal", on_delete=models.CASCADE)
    nominal = models.FloatField(null=False, blank=False)
    paid_period = models.CharField(max_length=20, null=False, blank=False)

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

    def __str__(self) -> str:
        return f"{self.user}, {self.portfolio_name}"
    
    class Meta:
        unique_together = ["user", "portfolio_name"]
