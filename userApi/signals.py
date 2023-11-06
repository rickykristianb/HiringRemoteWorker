from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db import connection
from .models import UserRate, Profile, Experience
from django.contrib.auth.models import User
from django.db.models import F, Func


def create_user(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            name=f"{user.first_name} {user.last_name}"
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


def count_total_exp(sender, instance, created, **kwargs):
        experience = instance
        if created:
            month_exp = int(str((experience.start_date - experience.end_date)/360 * 12).split(" ")[0].removeprefix("-"))
            experience.total_exp = month_exp
            experience.save()


post_save.connect(save_user_rating, sender=UserRate)
post_save.connect(create_user, sender=User)
post_save.connect(count_total_exp, sender=Experience)
post_save.connect(save_user, sender=Profile)