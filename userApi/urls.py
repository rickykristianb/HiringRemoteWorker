from django.urls import path
from . import views
from .utils import MyTokenObtainPairView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('get_user/', views.get_user, name='get_user'),
    path('get_skills/', views.get_skills, name='get_skills'),
    path('send_email/', views.send_email, name='send_email'),
    path('login/', views.login, name='login'),
]