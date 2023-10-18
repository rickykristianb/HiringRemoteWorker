from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register([Profile, Language, Skills, EmploymentType, UserRate, UserType])
