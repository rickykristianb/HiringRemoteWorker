from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.http import HttpResponse
from .models import Profile, Language, Skills
from .serializers import ProfileSerializer, SkillsSerializer

# Create your views here.


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
    
def get_experiences(request):
    ...
