from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication
from django.http import HttpResponse
from .models import Profile, Language, Skills, Experience
from .serializers import ProfileSerializer, SkillsSerializer
from django.conf import settings

from django.core.mail import send_mail
from django.template.loader import render_to_string

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.http import HttpRequest

import json


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
            print(err)
            context = {
                "error": "Could not send email"
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        else:
            context = {
                "success": "Your message has been sent to \n contact@rickykristianbutarbutar.com"
            }
            return Response(context, status=status.HTTP_200_OK)

@api_view(["GET", "POST"])
def login(request: HttpRequest):
    if request.method == "POST":
        data = json.load(request.body)
        print(data)
        username = request.POST.get("username")
        password = request.POST.get("password")
        print(username)
        try:
            user = User.objects.get(username=username)
            user = authenticate(request, username=username, password=password)
            if user:
                print(user)
                login(request, user)
                context = {
                        "success": "ada coy"
                    }
                # time.sleep(5)
                return JsonResponse(context)
            else:
                context = {
                    "error": "Username and password do not match"
                }
                # time.sleep(5)
                return JsonResponse(context, status=401)

        except User.DoesNotExist:
            print("TIDAK ADA USER")
            context = {
                "error": "User does not exist"
            } 
            return JsonResponse(context, status=404)
    # return HttpResponse("LOGIN")


def register():
    ...

def logout():
    ...

def user_view():
    ...
