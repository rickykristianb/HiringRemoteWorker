from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.http import HttpResponse
from .models import Profile, Language, Skills, Experience, Education, SkillLevel, UserSkillLevel
from .serializers import *
from .utils import UserListResultsSetPagination
from djoser.views import UserViewSet
from django.shortcuts import get_object_or_404
from rest_framework import generics
from itertools import chain
from django.db.models import Q

from django.core.mail import send_mail
from django.template.loader import render_to_string

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.db import connection
from CaptureData.external_api import LocationSearch
from functools import reduce
# DB ERROR
from django.db import DataError, IntegrityError

import json
from datetime import datetime

# CONSTANT VARIABLE
DAYS_IN_YEAR = 365.25

class CustomUserViewSet(UserViewSet):
    '''CREATE CUSTOM USER'''
    serializer_class = CustomUserCreateSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            # CustomUserCreateSerializer.validate
            return CustomUserCreateSerializer
        return super().get_serializer_class()


@api_view(["GET"])
def get_user(request):
    users = Profile.objects.all()
    serializer = ProfileSerializer(users, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def get_skills(request):
    try:
        skills = Skills.objects.all()
        if skills:
            serializer = SkillsSerializer(skills, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            context = {
                "message": "Skills not found"
            }
            return Response(context, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        context = {
            "error": str(e)
        }
        return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(["GET"])
def get_skill_level(request):
    try:
        skills_level = SkillLevel.objects.all()
        if skills_level:
            serializer = SkillLevelSerializer(skills_level, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            context = {
                "message": "Skills Level not found"
            }
            return Response(context, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        context = {
            "error": str(e)
        }
        return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_skills(request):
    try:
        data = request.data
        user = request.user
        user_profile = Profile.objects.get(user=user)

        skill_instance = Skills.objects.get(id=data["skillId"])
        skill_level_instance = SkillLevel.objects.get(id=data["skillLevelId"])
        try:
            user_skill_level = UserSkillLevel.objects.create(
                user = user_profile,
                skills = skill_instance,
                skill_level = skill_level_instance,
            )
            context = {
                "success": "User Skill successfully saved",
                "id": user_skill_level.id
            }
            return Response(context, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": f"You have already added {skill_instance}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        return Response({"error": e}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def remove_skill(request, id):
    try:
        user = request.user
        user_profile = Profile.objects.get(user=user)
        skill_level = UserSkillLevel(user=user_profile, id=id)
        skill_level.delete()
        return Response({"success": "Successfully remove skills"},status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_skill_and_level(request):
    try:
        user = request.user
        user_profile = Profile.objects.get(user=user)
        user_skill_level = UserSkillLevel.objects.filter(user=user_profile)
        serializer = UserSkillLevelSerializer(user_skill_level, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
def get_user_profile(request, id):
    try:
        print("ID", id)
        user = Profile.objects.get(id=id)
        serializer = ProfileSerializer(user, many=False, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        print(str(e))

@api_view(["GET"])
@permission_classes({IsAuthenticated})
def get_login_user_type(request):
    try:
        user = request.user
        profile = Profile.objects.get(user=user)
        serializer = ProfileSerializer(profile, many=False)
        return Response(serializer.data["usertype"], status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_profile_image_name(request):
    user = request.user
    user_profile = get_object_or_404(Profile, email=user)
    serializer = ProfileSerializer(user_profile, many=False, context={'request': request})
    context = {
        "user_id": serializer.data["id"],
        "profile_picture": serializer.data["profile_picture"],
        "username": serializer.data["username"]
    }
    return Response(context, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_profile(request, id):
    try:
        user = get_object_or_404(User, id=id)
        user_profile = get_object_or_404(Profile, user=user)
        serializer = ProfileSerializer(user_profile, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(["GET"])
def get_all_candidate_profile(request):
    try:
        user = UserAccount.objects.filter(user_type="personal")
        # user_profile = Profile.objects.filter(user__in=user)
        # print(ProfileSerializer(user_profile, many=True).data)
        user_profile = Profile.objects.filter(
            Q(user__in=user, 
              userskilllevel__isnull=False, 
              userlocation__isnull=False, 
              expectedsalary__isnull=False, 
              useremploymenttype__isnull=False, 
              short_intro__isnull=False)
            ).distinct()
        
        total_user_list= user_profile.count()
        # data = [x for x in serializer.data if (x["skills"] != [] and x["userlocation"] is not None and x["expectedsalary"] is not None and x["useremploymenttype"] != [] and x["short_intro"] is not None) ]
        paginator = UserListResultsSetPagination()
        result_page = paginator.paginate_queryset(user_profile, request)
        serializer = ProfileSerializer(result_page, many=True)
        context = {
            "data": serializer.data,
            "total_user": total_user_list
        }
        return Response(context, status=status.HTTP_200_OK)
    except Exception as e:
        # print("..............................")
        # print(str(e))
        return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def save_profile(request):
    try:
        data = request.data
        request_user = request.user
        try:
            user_profile = Profile.objects.get(user=request_user)
        except Exception as e:
            return Response({"error": e}, status=status.HTTP_404_NOT_FOUND)
        else:
            user_profile.name = data["name"]
            user_profile.short_intro = data["shortIntro"]
            user_profile.bio = data["bio"]
            user_profile.phone_number = data["phoneNumber"]
            try:
                user_profile.save()
                return Response({"success": "Profile saved"}, status=status.HTTP_201_CREATED)
            except Exception as e:
                error_info = {
                    'error_type': type(e).__name__,
                    'error_message': str(e),
                }
                json_error_info = json.dumps(error_info["error_message"])
                if data["phoneNumber"] in json_error_info:
                    return Response({"error": f"{data["phoneNumber"]} already in used by another user, try another number"}, status=status.HTTP_400_BAD_REQUEST)
                return Response({"error": json_error_info}, status=status.HTTP_400_BAD_REQUEST)
                
    except Exception as e:
        return Response({"error": e}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_education(request):
    try:
        user = request.user
        user_profile = get_object_or_404(Profile, user=user)
        data = request.data

        new_education = Education(user=user_profile)
        new_education.major = data.get("major", "")
        new_education.school_name = data.get("schoolName", "")
        new_education.degree = data.get("degree", "")
        new_education.save()

        # Include the newly generated UUID in the response
        response_data = {
            "success": "Education added successfully",
            "id": str(new_education.id)  # Convert the UUID to a string
        }

        return Response(response_data, status=status.HTTP_201_CREATED)  # 201 indicates resource creation
    except Exception as e:
        return Response({"error": e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def edit_education(request, id):
    try:
        data = request.data
        try:
            education = Education.objects.get(id=id)
            education.major = data["major"]
            education.school_name = data["school_name"]
            education.degree = data["degree"]
            education.save()
            return Response({"success": "Education saved"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
    return Response({"OK": "OK"})


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_education(request, id):
    try:
        user = request.user
        user_profile = get_object_or_404(Profile, user=user)

        education = Education.objects.filter(id=id, user=user_profile)
        education.delete()
        return Response({"success": "Education deleted"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error", e}, status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_education(request):
    user = request.user
    user_profile = get_object_or_404(Profile, user=user)
    education = Education.objects.filter(user=user_profile)
    serializer = EducationSerializer(education, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_languages(request):
    user = request.user
    user_profile = Profile.objects.get(user=user)
    language = Language(user=user_profile)
    serializer = LanguageSerializer(language, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_language(request):
    try:
        user = request.user
        user_profile = get_object_or_404(Profile, user=user)
        try:
            data = request.data
            new_language = Language(user=user_profile)
            new_language.language = data["language"]
            new_language.proficiency = data["proficiency"]
            new_language.save()

            response_data = {
                "success": "Education added successfully",
                "id": str(new_language.id)  # Convert the UUID to a string
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"You have already added {data["language"]}"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def remove_language(request, id):
    try:
        user = request.user
        user_profile = Profile.objects.get(user=user)
        language = Language(user=user_profile, id=id)
        try:
            language.delete()
            return Response({"success": "Your language has been removed"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": e}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": e}, status=status.HTTP_404_NOT_FOUND)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def save_user_image(request):
    user = request.user
    user_profile = Profile.objects.get(user=user)
    uploaded_file = request.FILES.get('image')
    if uploaded_file:
        user_profile.profile_picture = uploaded_file
        try:
            user_profile.save()
            serializer = ProfileSerializer(user_profile, many=False, context={'request': request})
            context = {
                "profile_image": serializer.data["profile_picture"]
            }
            return Response(context, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({"error": "No image provided"}, status=status.HTTP_400_BAD_REQUEST)
    


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_experience(request):
    date = datetime.now().date()
    user = request.user
    try:
        user_profile = get_object_or_404(Profile, user=user)
        if user_profile:
            data = request.data
            new_experience = Experience(user=user_profile)
            new_experience.job_name = data["jobTitle"]
            new_experience.company_name = data["companyName"]
            new_experience.start_date = data["jobStartDate"]
            try:
                new_experience.end_date = data["jobEndDate"]
            except Exception as e:
                new_experience.end_date = "9999-12-31"
            new_experience.details = data.get("jobDescription", "")
            try:
                new_experience.save()
                response_data = {
                    "success": "Experience added successfully",
                    "id": str(new_experience.id)  # Convert the UUID to a string
                }
                return Response(response_data , status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": e}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": "User profile not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(["UPDATE", "PATCH"])
@permission_classes([IsAuthenticated])
def save_experience(request, id):
    data = request.data
    try:
        experience = Experience.objects.get(id=id)
        experience.job_name = data["jobTitle"]
        experience.company_name = data["companyName"]
        experience.start_date = data["jobStartDate"]
        experience.end_date = data["jobEndDate"]
        experience.details = data["jobDescription"]
        experience.save()
        return Response({"success": "Experience saved"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)


# @api_view(["GET"])
# @permission_classes([IsAuthenticated])
# def get_experience(request):
#     print("MASKKK")
#     try:
#         user = request.user
#         user_profile = Profile.objects.get(user=user)
#         experience = Experience.objects.filter(user=user_profile).order_by("-end_date")
#         print(experience)
#         serializer = ExperienceSerializer(experience, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     except Exception as e:
#         return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_experience(request, id):
    try:
        user = request.user
        user_profile = Profile.objects.get(user=user)
        try:
            experience = Experience.objects.filter(user=user_profile, id=id)
            experience.delete()
            return Response({"success": "Experience deleted"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": e}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": e}, status=status.HTTP_404_NOT_FOUND)
    

#  Employment Type
@api_view(["GET"])
def get_employment_type(request):
    try:
        employment_type = EmploymentType.objects.all()
        serializer = EmploymentTypeSerializer(employment_type, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": e}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_employment_type(request):
    try:
        user = request.user
        user_profile = Profile.objects.get(user=user)
        employment_type = UserEmploymentType.objects.filter(user=user_profile)
        serializer = UserEmploymentTypeSerializer(employment_type, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_employment_type(request):
    try:
        user = request.user
        user_profile = Profile.objects.get(user=user)
        data = request.data
        employment_type = EmploymentType(id=data["id"])
        try:
            UserEmploymentType.objects.create(user=user_profile, employment_type=employment_type)
            return Response({"success": "Employment type added"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": f"You have selected {data["value"]}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except  Exception as e:
        return Response({"error": e}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def remove_emp_type(request, id):
    try:
        user = request.user
        user_profile = Profile.objects.get(user=user)
        emp_type = EmploymentType.objects.get(id=id)
        try:
            user_emp_type = UserEmploymentType.objects.filter(user=user_profile, employment_type=emp_type)
            user_emp_type.delete()
            return Response({"success": f"{emp_type.type} deleted"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": e}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_portfolio(request):
    try:
        user = request.user
        data = request.data
        user_profile = Profile.objects.get(user=user)
        try:
            new_portfolio = Portfolio.objects.create(user=user_profile, portfolio_link=data["link"], portfolio_name=data["type"])
            context = {
                "success": "Link saved",
                "id": new_portfolio.id
            }
            return Response(context, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": f"You have already added {data["type"]}"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_portfolio(request, id):
    try:
        user = request.user
        user_profile = Profile.objects.get(user=user)
        try:
            portfolio = Portfolio.objects.get(user=user_profile, id=id)
            portfolio.delete()
            return Response({"success": f"{portfolio.portfolio_name} Deleted"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": e}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def save_portfolio(request):
    try:
        user = request.user
        user_profile = Profile.objects.get(user=user)
        data = request.data
        if data.get("link") != "":
            try:
                portfolio = Portfolio.objects.get(user=user_profile, id=data["id"])
                portfolio.portfolio_link = data.get("link")
                portfolio.save()
                return Response({"success": f"{data.get("type")} is saved"}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": e}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"errorField": "Link is Empty"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_rate(request):
    try:
        user = request.user
        user_profile = Profile.objects.get(user=user)
        data = request.data
        try:
            expected_salary = ExpectedSalary.objects.create(
                user=user_profile,
                nominal=float(data["amount"]),
                paid_period=data["period"])
            return Response({"success": "Rate added"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": "You have already added your rate"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def save_rate(request):
    try:
        user = request.user
        user_profile = Profile.objects.get(user=user)
        try:
            expected_salary = ExpectedSalary.objects.get(user=user_profile)
            data = request.data
            expected_salary.nominal = data["amount"]
            expected_salary.paid_period = data["period"]
            expected_salary.save()
            return Response({"success": "New rate is saved"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(["GET"])
def get_location(request):
    location = Location.objects.all()
    serializer = LocationSerializer(location, many=True)
    sorted_location = sorted(serializer.data, key=lambda data: data['location'])
    return Response(sorted_location)


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def save_location(request):
    try:
        user = request.user
        data = request.data
        user_profile = Profile.objects.get(user=user)
        location = get_object_or_404(Location, id=data)
        save_location = UserLocation.objects.get_or_create(user=user_profile)
        save_location[0].location = location
        try:
            save_location[0].save()
            return Response({"success": "Location saved"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"Failed to save location, {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
def search_bar_data(request):
    data = {}
    skills = Skills.objects.all()
    skills_serializer = SkillsSerializer(skills, many=True)
    skill_data = [data["skill_name"] for data in skills_serializer.data]
    
    emp_type = EmploymentType.objects.all()
    emp_type_serializer = EmploymentTypeSerializer(emp_type, many=True)
    emp_type_data = [data["type"] for data in emp_type_serializer.data]

    location = Location.objects.all()
    location_serializer = LocationSerializer(location, many=True)
    location_data = [data["location"] for data in location_serializer.data]
    
    data["skills"] = skill_data
    data["emp_type"] = emp_type_data
    data["location"] = location_data

    return Response(data, status=status.HTTP_200_OK)


@api_view(["POST"])
def search_result(request):
    data = request.data
    user = UserAccount.objects.filter(user_type="personal")
    user_profile = Profile.objects.filter( 
        Q(user__in=user, 
            userskilllevel__isnull=False, 
            userlocation__isnull=False, 
            expectedsalary__isnull=False, 
            useremploymenttype__isnull=False) &
        (Q(userskilllevel__skills__skill_name__icontains=data) |
        Q(useremploymenttype__employment_type__type__icontains=data)|
        Q(userlocation__location__location__icontains=data)) &
        Q(short_intro__isnull=False)
    ).distinct()
    
    paginator = UserListResultsSetPagination()
    result_page = paginator.paginate_queryset(user_profile, request)
    serializer = ProfileSerializer(result_page, many=True)
    context = {
        "data": serializer.data,
        "total_user": len(user_profile)
    }

    return Response(context, status=status.HTTP_200_OK)

def min_max_year_counter(min, max):
    years_min = min * DAYS_IN_YEAR
    years_max = max * DAYS_IN_YEAR
    return [years_min, years_max]

@api_view(["GET"])
def advance_search_result(request):
    try:
        min_rate = 0
        final_result = []

        # GET SKILLS DATA FROM CLIENT
        skills = set(request.GET.get("skill").split(","))
        skills_condition = "" if "" in skills else "HAVING COUNT(b2.skill_name) = %s"
        # IF NO SKILLS DATA FROM CLIENT, RETRIEVE ALL SKILLS LISTED IN DATABASE
        if "" in skills:
            all_skills = Skills.objects.all()
            skills = set(skill.skill_name for skill in all_skills)

        # GET LOCATION DATA FROM CLIENT
        location = set(request.GET.get("location").split(","))
        # IF NO LOCATION DATA FROM CLIENT, RETRIEVE ALL SKILLS LISTED IN DATABASE      
        if "" in location:
            all_location = Location.objects.all()
            location = set(location.location for location in all_location)

        # GET RATE DATA FROM CLIENT
        rate = set(request.GET.get("rate", ""))
        # IF NO RATE DATA FROM CLIENT, RETRIEVE ALL PROFILE WITH RATE GREATER OR EQUAL THAN 1
        if not rate:
            min_rate = 1
        else:
            # CLEAN RATE CAPTURED FROM THE CLIENT
            new_rate = {i for i in rate if i != "," }
            min_rate = min(new_rate)

        raw_query = f"""
            WITH user_profile as
                (SELECT * FROM userapi_useraccount WHERE user_type="personal"),
                user_profile_rate as
                    (SELECT ua1.* FROM user_profile p1
                    INNER JOIN userapi_profile ua1 ON p1.email=ua1.email
                    WHERE ua1.rate_ratio >= %s
                    AND short_intro IS NOT NULL),
                user_profile_skill as
                    (SELECT a1.id as user_id FROM user_profile_rate a1
                    INNER JOIN userapi_userskilllevel b1 ON a1.id=b1.user_id
                    INNER JOIN userapi_skills b2 ON b2.id=b1.skills_id
                    WHERE b2.skill_name IN %s
                    GROUP BY a1.id
                    {skills_condition}),
                user_location as
                    (SELECT a2.user_id, b4.location FROM user_profile_skill a2
                    INNER JOIN userapi_userlocation b3 ON a2.user_id=b3.user_id
                    INNER JOIN userapi_location b4 ON b3.location_id=b4.id
                    WHERE b4.location IN %s
                    AND b4.location IS NOT NULL)
                    
                    SELECT b5.* FROM user_location a3
                    INNER JOIN userapi_profile b5 ON a3.user_id=b5.id
                    ;
            """
        if skills_condition != "":
            user_profiles = Profile.objects.raw(raw_query, [min_rate, list(skills), len(skills), list(location)])
        else:
            user_profiles = Profile.objects.raw(raw_query, [min_rate, list(skills), list(location)])


        experience = request.GET.get("experience", "")
        if experience != "[object Object]" and experience != "undefined":

            if experience == "1 - 2 years":
                years_min, years_max = min_max_year_counter(1, 2)
            elif experience == "2 - 4 years":
                years_min, years_max = min_max_year_counter(2, 4)
            elif experience == "4 - 6 years":
                years_min, years_max = min_max_year_counter(4, 6)
            elif experience == "6 - 8 years":
                years_min, years_max = min_max_year_counter(6, 8)
            elif experience == "8 - 10 years":
                years_min, years_max = min_max_year_counter(8, 10)
            elif experience == "> 10 years":
                years_min, years_max = min_max_year_counter(10, 100)
            serializer = ProfileSerializer(user_profiles, many=True)

            for data in serializer.data:
                total_exp = float(data["experiences"]["total_exp"])
                if years_min <= total_exp <= years_max:  
                    final_result.append(data)
        else:
            result = ProfileSerializer(user_profiles, many=True).data
            for data in result:
                if data["useremploymenttype"] != []:
                    final_result.append(data)

        paginator = UserListResultsSetPagination()
        result_page = paginator.paginate_queryset(final_result, request)
        context = {
            "data": result_page,
            "total_user": len(final_result)
        }
        return Response(context, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def save_company_profile(request):
    import time
    # time.sleep(5)
    try:
        data = request.data
        user = request.user
        user_profile = Profile.objects.get(user=user)
        user_location = UserLocation.objects.get_or_create(user=user_profile)
        user_profile.name = data.get("name", "")
        user_profile.email = data.get("email", "")
        user_profile.phone_number = data.get("phoneNumber", "")
        user_profile.address = data.get("address", "")
        user_profile.bio = data.get("bio", "")
        print(data.get("location"))
        location_id = get_object_or_404(Location, id=data.get("location", ""))
        
        user_location[0].location = location_id
        user_location[0].save()
        user_profile.save()
        return Response({"success": "Company profile saved"}, status=status.HTTP_200_OK)
    except DataError as e:
        if e.args[0] == 1406:
            return Response({"error": "Phone Number is too long"}, status=status.HTTP_400_BAD_REQUEST)
    except IntegrityError as e:
        if e.args[0] == 1062:
            return Response({"error": "Phone Number is already in used, try another"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(str(e))
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)