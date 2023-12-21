from django.urls import path
from . import views 
from djoser.views import UserViewSet
from .views import CustomUserViewSet
from .utils import MyTokenObtainPairView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    # TOKEN
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # USER
    path('get_user/', views.get_user, name='get_user'),

    # PROFILE
    path('profile/<str:id>', views.get_user_profile, name='get_user_profile'),
    path('get_all_candidate_profile/', views.get_all_candidate_profile, name='get_all_candidate_profile'),
    path('profile_image_name/', views.get_profile_image_name, name='get_profile_image_name'),
    # path('profile/<str:id>/', views.get_profile, name='get_profile'),
    path('save_profile/', views.save_profile, name='save_profile'),
    path('save_user_image/', views.save_user_image, name='save_user_image'),
    # SKILLS
    path('get_user_skills/', views.get_user_skill_and_level, name='get_user_skill_and_level'),
    path('get_skills/', views.get_skills, name='get_skills'),
    path('get_skill_level/', views.get_skill_level, name='get_skill_level'),
    path('add_skills/', views.add_skills, name='add_skills'),
    path('delete_skills/<str:id>/', views.remove_skill, name='remove_skill'),
    # EXPERIENCE
    path('add_experience/', views.add_experience, name='add_experience'),
    # path('get_experience/', views.get_experience, name='get_experience'),
    path('save_experience/<str:id>', views.save_experience, name='save_experience'),
    path('delete_experience/<str:id>', views.delete_experience, name='delete_experience'),
    # EDUCATION
    path('add_education/', views.add_education, name='add_education'),
    path('delete_education/<str:id>/', views.delete_education, name='delete_education'),
    path('get_education/', views.get_education, name='get_education'),
    path('edit_education/<str:id>/', views.edit_education, name='edit_education'),
    # LANGUAGE
    path('add_language/', views.add_language, name='add_language'),
    path('remove_language/<str:id>', views.remove_language, name='remove_language'),
    # EMPLOYMENT TYPE
    path('get_emp_type/', views.get_employment_type, name='get_employment_type'),
    path('user_emp_type/', views.get_user_employment_type, name='get_user_employment_type'),
    path('add_user_emp_type/', views.add_employment_type, name='add_user_emp_type'),
    path('remove_emptype/<str:id>/', views.remove_emp_type, name='remove_emp_type'),
    # PORTFOLIO
    path('add_portfolio/', views.add_portfolio, name='add_portfolio'),
    path('remove_portfolio/<str:id>/', views.delete_portfolio, name='delete_portfolio'),
    path('save_portfolio/', views.save_portfolio, name='save_portfolio'),
    #RATE
    path('add_rate/', views.add_rate, name='add_rate'),
    path('save_rate/', views.save_rate, name='save_rate'),
    # LOCATION
    path('get_location/', views.get_location, name='get_location'),
    path('save_location/', views.save_location, name='save_location'),
    # SEARCH
    path('search_bar_data/', views.search_bar_data, name='search_bar_data'),
    path('search_result/', views.search_result, name='search_result'),
    path('advance_search_result/', views.advance_search_result, name='advance_search_result'),
    # Custom url for creating user, not using regular api url /auth/users to create new
    path('auth/create_user/', CustomUserViewSet.as_view({"post": "create", "get": "list"}), name="user-register")
]