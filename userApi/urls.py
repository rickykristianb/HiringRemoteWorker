from django.urls import path
from . import views

urlpatterns = [
    path('get_user/', views.get_user, name='get_user'),
    path('get_skills/', views.get_skills, name='get_skills')
]