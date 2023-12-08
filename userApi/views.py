from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.http import HttpResponse
from .models import Profile, Language, Skills, Experience, Education, SkillLevel, UserSkillLevel
from .serializers import *
from .utils import MessagesResultsSetPagination
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

import json
from datetime import datetime

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


@api_view(["POST"])
def send_email(request):
    if request.method == "POST":
        subject="Email From Portfolio Website",
        from_email = request.data["email"]
        to_email = "contact@rickykristianbutarbutar.com"
        name = request.data["name"]
        message_body = request.data["messageBody"].split("\n")

        context = {
                    "name": name,
                    "from_email": from_email,
                    "message": message_body
                }
        
        message=render_to_string("send_mail.html", context)

        try:
            send_mail(
                subject[0],
                message,
                from_email,
                [to_email],
                fail_silently=False, 
                html_message=message
                )
        except Exception as err:
            context = {
                "error": "Could not send email"
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        else:
            context = {
                "success": "Your message has been sent to \n contact@rickykristianbutarbutar.com"
            }
            return Response(context, status=status.HTTP_200_OK)

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
@permission_classes([IsAuthenticated])
def get_login_user_profile(request):
    user = request.user
    user_profile = get_object_or_404(Profile, email=user)
    serializer = ProfileSerializer(user_profile, many=False, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_profile_image_name(request):
    user = request.user
    user_profile = get_object_or_404(Profile, email=user)
    serializer = ProfileSerializer(user_profile, many=False, context={'request': request})
    context = {
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
            user_profile.save()
            return Response({"success": "Profile saved"},status=status.HTTP_201_CREATED)
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


@api_view(["PATCH"])
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
        try:
            experience.save()
            return Response({"success": "Experience saved"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": e}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": e}, status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_experience(request):
    try:
        user = request.user
        user_profile = Profile.objects.get(user=user)
        experience = Experience.objects.filter(user=user_profile).order_by("-end_date")
        serializer = ExperienceSerializer(experience, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    

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
    

# MESSAGES
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def send_message(request):
    try:
        user = request.user
        data = request.data
        user_profile = Profile.objects.get(user=user)
        serializer = ProfileSerializer(user_profile)
        try:
            recipient = Profile.objects.get(user__email=(data.get("to_user")).lower())

            Message.objects.create(
                sender=user_profile, 
                recipient=recipient,
                name=serializer.data["name"],
                email=serializer.data["email"],
                subject=data.get("subject"),
                body=data.get("message_body"),
                created=datetime.now())
            return Response({"success": "Message send"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": f"Recipient {data.get("to_user").lower()} not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def send_reply_message(request):
    try:
        user = request.user
        data = request.data
        user_profile = Profile.objects.get(user=user)
        serializer = ProfileSerializer(user_profile)
        message_body = data["formData"]["message_body"]
        recipient_reply_data = data["reply_data"]
        try:
            msg_recipient = Profile.objects.get(user__email=(recipient_reply_data["sender"]["email"]).lower())
            Message.objects.create(
                sender=user_profile, 
                recipient=msg_recipient,
                name=msg_recipient.name,
                email=msg_recipient.email,
                subject=recipient_reply_data["subject"],
                body=message_body,
                prev_reply_message=recipient_reply_data["body"],
                created=datetime.now())
            return Response({"success": "Message sent"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": f"Recipient {data.get("to_user").lower()} not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_message(request):
    try:
        user = request.user
        user_profile = Profile.objects.get(user=user)
        message = Message.objects.filter(recipient=user_profile, is_deleted_by_recipient=False)
        count_is_read = message.filter(is_read=False).count()
        serializer = MessageSerializer(message, many=True)
        
        context = {
            "data": serializer.data,
            "is_read_count": count_is_read
        }
        return Response(context, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def on_read_message(request, id):
    try:
        user = request.user
        user_profile = Profile.objects.get(user=user)
        message = Message.objects.get(recipient=user_profile, id=id)
        message.is_read = True
        message.date_read = datetime.now()
        message.save()
        return Response({"success": "read"},status=status.HTTP_202_ACCEPTED)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_message(request, id):
    try:
        user = request.user
        try:
            user_profile = Profile.objects.get(user=user)
            message = Message.objects.get(recipient=user_profile, id=id)
            message.is_deleted_by_recipient = True
            message.save()
            return Response({"success": "Message deleted"}, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def delete_message_forever(request, id):
    try:
        user = request.user
        user_profile = Profile.objects.get(user=user)
        try:
            delete_message_forever = Message.objects.get(recipient=user_profile, id=id)
            MessageDeleted.objects.create(message=delete_message_forever)
        except Exception as e:
            delete_message_forever = Message.objects.get(sender=user_profile, id=id)
            MessageDeleted.objects.create(message=delete_message_forever)
        finally:
            return Response({"success": "Message deleted forever."}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_deleted_messages(request):
    try:
        user = request.user
        user_profile = Profile.objects.get(user=user)
        deleted_messages = Message.objects.filter(
                Q(recipient=user_profile, is_deleted_by_recipient=True) |
                Q(sender = user_profile, is_deleted_by_sender = True,)
        ).exclude(
            Q(messagedeleted__deleted_at__isnull=False)
        )
        serializer = MessageSerializer(deleted_messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        serializer = MessageSerializer(deleted_messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_sent_messages(request):
    try:
        user = request.user
        user_profile = Profile.objects.get(user=user)
        message = Message.objects.filter(sender=user_profile, is_deleted_by_sender=False)
        count_is_read = message.filter(is_read=False).count()
        serializer = MessageSerializer(message, many=True)
        context = {
            "data": serializer.data,
            "is_read_count": count_is_read
        }
        return Response(context, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def delete_sent_message(request, id):
    try:
        user = request.user
        user_profile = Profile.objects.get(user=user)
        message = Message.objects.get(sender=user_profile, id=id)
        message.is_deleted_by_sender = True
        message.save()
        return Response({"success": "Sent message has been deleted"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_total_inbox_message(request):
    try:
        user = request.user
        user_profile = Profile.objects.get(user=user)
        total_inbox_message = Message.objects.filter(recipient=user_profile, is_deleted_by_recipient=False).count()
        return Response({"total": total_inbox_message}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_inbox_pagination(request):
    '''GET MESSAGES BASED ON PAGE PAGINATED'''
    try:
        user = request.user
        user_profile = Profile.objects.get(user=user)
        message = Message.objects.filter(recipient=user_profile, is_deleted_by_recipient=False)
        total_inbox_message = Message.objects.filter(recipient=user_profile, is_deleted_by_recipient=False).count()
                
        # PAGINATOR
        paginator = MessagesResultsSetPagination()
        result_page = paginator.paginate_queryset(message, request)
        serializer = MessageSerializer(result_page, many=True)

        context = {
            "data": serializer.data,
            "total_inbox": total_inbox_message
        }

        return Response(context, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def count_unread_messages(request):
    '''FOR INBOX UNREAD MESSAGE NOTIFICATION'''
    user = request.user
    user_profile = Profile.objects.get(user=user)
    message = Message.objects.filter(recipient=user_profile, is_read=False, is_deleted_by_recipient=False).count()
    return Response(message)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_sent_message_pagination(request):
    '''GET SENT MESSAGES BASED ON PAGE PAGINATED'''
    try:
        user = request.user
        user_profile = Profile.objects.get(user=user)
        message = Message.objects.filter(sender=user_profile, is_deleted_by_sender=False)
        total_sent_message = Message.objects.filter(sender=user_profile, is_deleted_by_sender=False).count()
        # PAGINATOR
        paginator = MessagesResultsSetPagination()
        result_page = paginator.paginate_queryset(message, request)
        serializer = MessageSerializer(result_page, many=True)

        context ={
            "data": serializer.data,
            "total_sent_message": total_sent_message
        }

        return Response(context, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_deleted_message_pagination(request):
    '''GET DELETED MESSAGES BASED ON PAGE PAGINATED'''
    try:
        user = request.user
        user_profile = Profile.objects.get(user=user)
        deleted_messages = Message.objects.filter(
                Q(recipient=user_profile, is_deleted_by_recipient=True) |
                Q(sender = user_profile, is_deleted_by_sender = True,)
        ).exclude(
            Q(messagedeleted__deleted_at__isnull=False)
        )

        total_deleted_message = deleted_messages.count()

        # PAGINATOR
        paginator = MessagesResultsSetPagination()
        result_page = paginator.paginate_queryset(deleted_messages, request)
        serializer = MessageSerializer(result_page, many=True)

        context_page = {
            "data": serializer.data,
            "total_deleted_message": total_deleted_message
        }

        return Response(context_page, status=status.HTTP_200_OK)
    except Exception as e:
        serializer = MessageSerializer(deleted_messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


    


    


