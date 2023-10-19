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

    NATIVE = "native"
    EXPERT = "expert"
    FLUENT = "fluent"
    INTERMEDIATE = "intermediate"
    BEGINNER = "beginner"
    PROFICIENCY_CHOICES = [
        (NATIVE, "Native"),
        (EXPERT, "Expert"),
        (FLUENT, "Fluent"),
        (INTERMEDIATE, "Intermediate"),
        (BEGINNER, "Beginner")
    ]
    proficiency = models.IntegerField(choices=PROFICIENCY_CHOICES, default=NATIVE)
    
    def __str__(self) -> str:
        return f"{self.language}, {self.user}, {self.proficiency}"
    
    class Meta:
        unique_together = ["user", "language"]
    

class Skills(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    skill_name = models.CharField(max_length=20, null=True, blank=True)

    NOVICE = "novice"
    BEGINNER = "beginner"
    ADVANCE_BEGINNER = "advance_beginner"
    COMPETENT = "competent"
    PROFICIENT = "proficient"
    EXPERT = "expert"
    SKILL_LEVEL_CHOICES = [
        (NOVICE, "Novice"), 
        (BEGINNER, "Beginner"), 
        (ADVANCE_BEGINNER, "Advanced Beginner"),
        (COMPETENT, "Competent"),
        (PROFICIENT, "Proficient"),
        (EXPERT, "Expert")
    ]
    skill_level = models.IntegerField(choices=SKILL_LEVEL_CHOICES, default=NOVICE)

    def __str__(self) -> str:
        return f"{self.user}, {self.skill_name}, {self.skill_level}"
    
    
class EmploymentType(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=False)
    FULL_TIME_CONTRACT = "fulltime_contract"
    FULL_TIME_PERMANENT = "fulltime_permanent"
    TYPE_CHOICES = [
        (FULL_TIME_CONTRACT, "Full-time/Contract"),
        (FULL_TIME_PERMANENT, "Full-time/Permanent")
    ]
    type_name = models.IntegerField(choices=TYPE_CHOICES, default=1)

    @property
    def get_type_name(self):
        return dict(self.TYPE_CHOICES).get(int(self.type_name))

    def __str__(self) -> str:
        return f"{self.user}, {self.get_type_name}, {self.type_name}"
    
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

    PERSONAL = "personal"
    COMPANY = "company"
    TYPE_CHOICES = [
        (PERSONAL, "Personal"),
        (COMPANY, "Company")
    ]
    type_name = models.IntegerField(choices=TYPE_CHOICES, default=PERSONAL)

    def __str__(self) -> str:
        return f"{self.user}, {self.type_name}"
    
class Education(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    user = models.ForeignKey(User, null=False, blank=False, default="Personal", on_delete=models.CASCADE)
    major = models.CharField(max_length=50, null=True, blank=True)
    DEGREE_CHOICES =[
        (1, "Diploma"),
        (2, "Bachelor"),
        (3, "Postgraduate")
    ]
    degrees = models.IntegerField(choices=DEGREE_CHOICES, default=1)
    school_name = models.CharField(max_length=100, null=True, blank=True)
    start_year = models.DateField()
    end_year = models.DateField()

    def __str__(self) -> str:
        return f"{self.user}, {self.major}, {self.degrees}"
    
class ExpectedSalary(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user = models.OneToOneField(User, null=False, blank=False, default="Personal", on_delete=models.CASCADE)
    CURRENCY_CHOICES = [
        (1, "Rp"),
        (2, "$")
    ]
    currency = models.IntegerField(choices=CURRENCY_CHOICES, default=1)
    nominal = models.FloatField()
    PAID_PERIOD_CHOICES = [
        (1, "hourly"),
        (2, "monthly"),
        (3, "yearly")
    ]
    paid_period = models.IntegerField(choices=PAID_PERIOD_CHOICES, default=3)

    def __str__(self) -> str:
        return str(self.nominal)
    
class Experience(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user = models.ForeignKey(User, null=False, blank=False, default="Personal", on_delete=models.CASCADE)
    job_name = models.CharField(max_length=100, null=False, blank=False)
    company_name = models.CharField(max_length=100, null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    details = models.TextField(max_length=600, null=True, blank=True)
    total_exp = models.FloatField()

    def __str__(self) -> str:
        return f"{self.user}, {self.company_name}, {self.start_date}, {self.end_date}"
    
class Networking(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user = models.ForeignKey(User, null=False, blank=False, default="Personal", on_delete=models.CASCADE)
    networking_link = models.CharField(max_length=100, null=False, blank=False)
    NETWORKING_CHOICES = [
        (1, "LinkedIn"),
        (2, "Facebook"),
        (3, "Instagram"),
        (4, "Twitter")
    ]
    networking_name = models.IntegerField(choices=NETWORKING_CHOICES, null=False, blank=False, default=1)

    @property
    def get_network_name(self):
        return dict(self.NETWORKING_CHOICES).get(self.networking_name)

    def __str__(self) -> str:
        return f"{self.user}, {self.get_network_name}"
    
    class Meta:
        unique_together = ["user", "networking_name"]
    
class Portfolio(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user = models.ForeignKey(User, null=False, blank=False, default="Personal", on_delete=models.CASCADE)
    portfolio_link = models.CharField(max_length=100, null=False, blank=False)
    PORTFOLIO_CHOICES = [
        (1, "Github"),
        (2, "LinkedIn"),
        (3, "Personal Website"),
        (4, "Other Link")
    ]
    portfolio_name = models.IntegerField(choices=PORTFOLIO_CHOICES, null=False, blank=False, default=1)

    @property
    def get_portfolio_name(self):
        return dict(self.PORTFOLIO_CHOICES).get(self.portfolio_name)

    def __str__(self) -> str:
        return f"{self.user}, {self.get_portfolio_name}"
    
    class Meta:
        unique_together = ["user", "portfolio_name"]
