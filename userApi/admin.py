from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register([
    Profile, Language, Skills, SkillLevel, UserSkillLevel, ExpectedSalary,
    UserRate, Education, EmploymentType, UserEmploymentType,
    Experience, Networking, Portfolio,
    Message, MessageDeleted, UserAccount])
