from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from .utils import *

# Create your views here.
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_job(request):
    try:
        data = request.data
        user = request.user
        user_profile = Profile.objects.get(user=user)
        new_job = Jobs.objects.create(
            user_posted=user_profile,
            job_title= data.get("jobTitle"),
            job_detail = data.get("jobDetail"),
            experience_level = data.get("experienceLevel")
        )
        for skill in data.get("jobSkills"):
            skill_instance = Skills.objects.get(id=skill["id"])
            JobSkills.objects.create(
                job=new_job,
                skill = skill_instance
            )
        for type in data.get("jobEmploymentType"):
            employment_type_instance = EmploymentType.objects.get(id=type["id"])
            JobEmploymentType.objects.create(
                jobs=new_job,
                employment_type = employment_type_instance
            )
        for location in data.get("jobLocation"):
            location_instance = Location.objects.get(id=location["id"])
            JobLocation.objects.create(
                job=new_job,
                location=location_instance
            )
        JobSalaryRates.objects.create(
            job=new_job,
            nominal=data.get("jobSalary"),
            paid_period=data.get("jobSalaryPaidPeriod")
        )
        return Response({"success": "New job added"}, status=status.HTTP_201_CREATED)
    except Exception as e:
        print(str(e))
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(["GET"])
def get_all_posted_jobs(request, id):
    try:
        user_profile = Profile.objects.get(id=id)
        all_jobs = Jobs.objects.filter(user_posted=user_profile).order_by("-created_at")
        serializer = JobSerializer(all_jobs, many=True, context={'request': request})
        paginator = JobPostedPagination()
        result_page = paginator.paginate_queryset(serializer.data, request)
        context = {
            "data": result_page,
            "total_data": len(serializer.data)
        }
        return Response(context, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_authenticated_all_posted_jobs(request):
    try:
        user = request.user
        user_profile = Profile.objects.get(user=user)
        all_jobs = Jobs.objects.filter(user_posted=user_profile).order_by("-created_at")
        serializer = JobSerializer(all_jobs, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(["GET"])
def get_job_detail(request, id):
    try:
        job = Jobs.objects.get(id=id)
        serializer = JobSerializer(job, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

@api_view(["PATCH"])
@permission_classes({IsAuthenticated})
def update_job(request, id):
    try:
        data = request.data
        # print(data)
        job = Jobs.objects.get(id=id)
        job.status = data["jobStatus"]
        job.job_title = data["jobTitle"]
        job.job_detail = data["jobDetail"]
        job.experience_level = data["jobExperienceLevel"]
        job.save()

        job_skill = JobSkills.objects.filter(job=job)
        job_skill.delete()
        for skill in data.get("jobSkills"):
            skill_instance = Skills.objects.get(id=skill["skill"]["id"])
            JobSkills.objects.create(
                job=job,
                skill = skill_instance
            )
        
        job_location = JobLocation.objects.filter(job=job)
        job_location.delete()
        for location in data["jobLocation"]:
            location_instance = Location.objects.get(id=location["location"]["id"])
            JobLocation.objects.create(
                job=job,
                location=location_instance
            )
        
        job_employment_type = JobEmploymentType.objects.filter(jobs=job)
        job_employment_type.delete()
        for type in data["jobEmploymentType"]:
            type_instance = EmploymentType.objects.get(id=type["employment_type"]["id"])
            JobEmploymentType.objects.create(
                jobs=job,
                employment_type=type_instance
            )

        salary = JobSalaryRates.objects.get(job=job)
        salary.nominal = data["jobSalary"]
        salary.paid_period = data["jobSalaryPaidPeriod"]
        salary.save()

        return Response({"success": "Job is updated"}, status=status.HTTP_202_ACCEPTED)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_job(request, id):
    try:
        job = Jobs.objects.get(id=id)
        if job:
            job.delete()
            return Response({"success": "Job deleted"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)