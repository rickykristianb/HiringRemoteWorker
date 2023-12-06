from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db import connection
from .models import UserRate, Profile, Experience
# from django.contrib.auth.models import User

from django.db.models import F, Func
from datetime import datetime

from django.conf import settings
User = settings.AUTH_USER_MODEL


def create_user(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            email=user.email,
            name = user.name,
            username=user.username
        )
        profile.save()

def save_user(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user
    if created == False:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()


def save_user_rating(sender, instance, created, **kwargs):
    user_rate = instance
    profile = user_rate.to_user
    if created:
        user_rate = instance
        profile = user_rate.to_user
        profile.rate_total = F('rate_total') + user_rate.rate_value
        total_user_rate = UserRate.objects.filter(to_user=profile).count()
        profile.rate_ratio = profile.rate_total / total_user_rate
        profile.save()


# def count_total_exp(sender, instance, created, **kwargs):
#         experience = instance
#         if created:
#             start_date = datetime.strptime(experience.start_date, "%Y-%m-%d").date()
#             end_date = datetime.strptime(experience.end_date, "%Y-%m-%d").date()
#             print(end_date, start_date)
#             exp_days = int((str(end_date-start_date)).split()[0])
#             month_exp = exp_days / 360 * 12
#             experience.total_exp = month_exp / 12
#             experience.save()


post_save.connect(save_user_rating, sender=UserRate)
post_save.connect(create_user, sender=User)
# post_save.connect(count_total_exp, sender=Experience)
post_save.connect(save_user, sender=Profile)