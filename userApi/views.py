from django.shortcuts import render
from rest_framework.response import Response
from django.http import HttpResponse

# Create your views here.

def get_user(request):
    return HttpResponse("GOT IT")