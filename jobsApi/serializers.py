from rest_framework import serializers
from .models import *
from userApi.serializers import SkillsSerializer, EmploymentTypeSerializer, ProfileSerializer, LocationSerializer
from datetime import datetime

class JobEmploymentTypeSerializer(serializers.ModelSerializer):

    employment_type = EmploymentTypeSerializer()

    class Meta:
        model = JobEmploymentType
        fields = "__all__"

class JobSalaryRatesSerializer(serializers.ModelSerializer):

    class Meta:
        model = JobSalaryRates
        fields = "__all__"

class InterestedUsersSerializer(serializers.ModelSerializer):

    user = ProfileSerializer()

    class Meta:
        model = InterestedUsers
        fields = "__all__"

class JobLocationSerializer(serializers.ModelSerializer):

    location = LocationSerializer()

    class Meta:
        model = JobLocation
        fields = "__all__"

class JobSkillsSerializer(serializers.ModelSerializer):

    skill = SkillsSerializer()

    class Meta:
        model = JobSkills
        fields = "__all__"

class JobSerializer(serializers.ModelSerializer):

    user_posted = serializers.SerializerMethodField()
    user_profile_picture = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()
    jobsalaryrates = JobSalaryRatesSerializer()
    jobemploymenttype = serializers.SerializerMethodField()
    interesteduser = serializers.SerializerMethodField()
    joblocation = serializers.SerializerMethodField()
    jobskills = serializers.SerializerMethodField()

    class Meta:
        model = Jobs
        fields = "__all__"

    def get_user_posted(self, obj):
        context = {
            "id": obj.user_posted.id,
            "name":  obj.user_posted.name
        }
        return context
    
    def get_user_profile_picture(self, obj):
        user_posted = obj.user_posted

        if user_posted and user_posted.profile_picture:
            absolute_uri = self.context['request'].build_absolute_uri(user_posted.profile_picture.url)
        return absolute_uri
    
    def get_created_at(self, obj):
        created_at = str(obj.created_at)
        datetime_obj = datetime.fromisoformat(created_at)
        formatted_date = datetime_obj.strftime("%d-%m-%Y")
        return formatted_date
    
    def get_updated_at(self, obj):
        created_at = str(obj.updated_at)
        datetime_obj = datetime.fromisoformat(created_at)
        formatted_date = datetime_obj.strftime("%d-%m-%Y")
        return formatted_date

    def get_jobemploymenttype(self, obj):
        employmenttype = obj.jobemploymenttype_set.all()
        serializer = JobEmploymentTypeSerializer(employmenttype, many=True)
        return serializer.data
    
    def get_interesteduser(self, obj):
        interested_user = obj.interestedusers_set.all()
        serializer = InterestedUsersSerializer(interested_user, many=True)
        return serializer.data
    
    def get_joblocation(self, obj):
        location = obj.joblocation_set.all()
        serializer = JobLocationSerializer(location, many=True)
        return serializer.data
    
    def get_jobskills(self, obj):
        skills = obj.jobskills_set.all()
        serializer = JobSkillsSerializer(skills, many=True)
        return serializer.data