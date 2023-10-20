from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.http import HttpResponse
from .models import Profile
from .serializers import ProfileSerializer

# Create your views here.

@api_view(["GET"])
def get_user(request):
    users = Profile.objects.all()
    print(users)
    serializer = ProfileSerializer(users, many=True)
    print(serializer)
    return Response(serializer.data)