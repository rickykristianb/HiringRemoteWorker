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
    skills = models.ManyToManyField("Skills", blank=True)
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
    user = models.ManyToManyField(Profile, related_name='languages', blank=True)
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
    proficiency = models.CharField(max_length=20, choices=PROFICIENCY_CHOICES, default=NATIVE)
    
    def __str__(self) -> str:
        return f"{self.language}, {self.proficiency}"
    

class Skills(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
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
    skill_level = models.CharField(max_length=50, choices=SKILL_LEVEL_CHOICES, default=NOVICE)

    def __str__(self) -> str:
        return f"{self.skill_name}, {self.skill_level}"
    
    
class EmploymentType(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=False)
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
    type_name = models.CharField(max_length=50, choices=TYPE_CHOICES, default=FULL_TIME_CONTRACT)

    @property
    def get_type_name(self):
        return dict(self.TYPE_CHOICES).get(int(self.type_name))

    def __str__(self) -> str:
        return f"{self.user}, {self.get_type_name}, {self.type_name}"
    
    class Meta:
        unique_together = ["user", "type_name"]

class UserRate(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    user = models.ForeignKey(Profile, related_name="rating_owner", null=True, on_delete=models.SET_NULL)
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
    type_name = models.CharField(max_length=20, choices=TYPE_CHOICES, default=PERSONAL)

    def __str__(self) -> str:
        return f"{self.user}, {self.type_name}"
    
class Education(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    user = models.ForeignKey(Profile, null=False, blank=False, default="Personal", on_delete=models.CASCADE)
    major = models.CharField(max_length=50, null=True, blank=True)

    DIPLOMA = "diploma"
    BACHELOR = "bachelor"
    POSTGRADUATE = "postgraduate"
    DEGREE_CHOICES =[
        (DIPLOMA, "Diploma"),
        (BACHELOR, "Bachelor"),
        (POSTGRADUATE, "Postgraduate")
    ]
    degrees = models.CharField(max_length=20, choices=DEGREE_CHOICES, default=DIPLOMA)
    school_name = models.CharField(max_length=100, null=True, blank=True)
    start_year = models.DateField()
    end_year = models.DateField()

    def __str__(self) -> str:
        return f"{self.user}, {self.major}, {self.degrees}"
    
class ExpectedSalary(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user = models.OneToOneField(Profile, null=False, blank=False, default="Personal", on_delete=models.CASCADE)

    RUPIAH = "rp"
    USDOLLAR = "usd"
    CURRENCY_CHOICES = [
        (RUPIAH, "RP"),
        (USDOLLAR, "USD")
    ]
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default=RUPIAH)

    nominal = models.FloatField()
    HOURLY = "hourly"
    MONTHLY = "monthly"
    YEARLY = "yearly"
    PAID_PERIOD_CHOICES = [
        (HOURLY, "Hourly"),
        (MONTHLY, "Honthly"),
        (YEARLY, "Yearly")
    ]
    paid_period = models.CharField(max_length=20, choices=PAID_PERIOD_CHOICES, default=HOURLY)

    def __str__(self) -> str:
        return str(self.nominal)
    
class Experience(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user = models.ForeignKey(Profile, null=False, blank=False, default="Personal", on_delete=models.CASCADE)
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
    user = models.ForeignKey(Profile, null=False, blank=False, default="Personal", on_delete=models.CASCADE)
    networking_link = models.CharField(max_length=100, null=False, blank=False)
    NETWORKING_CHOICES = [
        (1, "LinkedIn"),
        (2, "Facebook"),
        (3, "Instagram"),
        (4, "Twitter")
    ]
    networking_name = models.CharField(max_length=20, choices=NETWORKING_CHOICES, null=False, blank=False, default=1)

    @property
    def get_network_name(self):
        return dict(self.NETWORKING_CHOICES).get(self.networking_name)

    def __str__(self) -> str:
        return f"{self.user}, {self.get_network_name}"
    
    class Meta:
        unique_together = ["user", "networking_name"]
    
class Portfolio(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user = models.ForeignKey(Profile, null=False, blank=False, default="Personal", on_delete=models.CASCADE)
    portfolio_link = models.CharField(max_length=100, null=False, blank=False)

    GITHUB = "github"
    LINKEDIN = "linkedin"
    PERSONAL_WEBSITE = "personal_website"
    OTHER_LINK = "other_link"
    PORTFOLIO_CHOICES = [
        (GITHUB, "Github"),
        (LINKEDIN, "LinkedIn"),
        (PERSONAL_WEBSITE, "Personal Website"),
        (OTHER_LINK, "Other Link")
    ]
    portfolio_name = models.CharField(max_length=20, choices=PORTFOLIO_CHOICES, null=False, blank=False, default=1)

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
