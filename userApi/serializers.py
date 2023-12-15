from rest_framework import serializers
from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
from .models import *

user_model = get_user_model()

class CustomUserCreateSerializer(UserCreateSerializer):
    # Custom user api field
    user_type = serializers.CharField(required=True)

    class Meta(UserCreateSerializer.Meta):
        model = user_model
        fields = ("id", "email", "name", "username", "password", "user_type")

        def validate(self, data):
            if data['password'] != data['re_password']:
                raise serializers.ValidationError("Passwords do not match.")
            return data


class UserRateSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserRate
        fields = "__all__"

class NetworkingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Networking
        exclude = ["user"]

class ExpectedSalarySerializer(serializers.ModelSerializer):

    class Meta:
        model = ExpectedSalary
        exclude = ["user"]

class PortfolioSerializer(serializers.ModelSerializer):

    class Meta:
        model = Portfolio
        exclude = ["user"]

class EducationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Education
        exclude = ["user"]

class ExperienceSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Experience
        fields = "__all__"

class SkillsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Skills
        fields = "__all__"

class SkillLevelSerializer(serializers.ModelSerializer):

    class Meta:
        model = SkillLevel
        fields = "__all__"


class LanguageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Language
        fields = "__all__"


class UserSkillLevelSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserSkillLevel
        fields = ["id", "skills", "skill_level"]

    skills = SkillsSerializer()
    skill_level = SkillLevelSerializer()

class EmploymentTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = EmploymentType
        fields = "__all__"

class UserEmploymentTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserEmploymentType
        fields = "__all__"
    
    employment_type = EmploymentTypeSerializer()

class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
        fields = "__all__"

class UserLocationSerializer(serializers.ModelSerializer):
    
    class Meta:
            model = UserLocation
            fields = "__all__"

    location = LocationSerializer()

class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = "__all__"

    skills = serializers.SerializerMethodField()
    languages = serializers.SerializerMethodField()
    experiences = serializers.SerializerMethodField()
    educations = serializers.SerializerMethodField()
    portfolios = serializers.SerializerMethodField()
    expectedsalary = ExpectedSalarySerializer(many=False)
    networkings = serializers.SerializerMethodField()
    userrate = serializers.SerializerMethodField()
    useremploymenttype = serializers.SerializerMethodField()
    userlocation = UserLocationSerializer()


    def get_skills(self, obj):
        level = ["expert", "advanced", "intermediate", "beginner"]
        skills = UserSkillLevel.objects.filter(user=obj)
        serializer = UserSkillLevelSerializer(skills, many=True)

        data_index = lambda x: level.index(x["skill_level"]["skill_level"].lower())
        sorted_data = sorted(serializer.data, key=data_index)
        return sorted_data

    def get_experiences(self, obj):
        experiences = obj.experience_set.all().order_by("-end_date")
        total_exp = 0
        for exp in experiences:
            total_exp += exp.total_exp
        serializer = ExperienceSerializer(experiences, many=True)
        context = {
            "data": serializer.data,
            "total_exp": "{:.2f}".format(total_exp)
        }
        return context
    
    def get_educations(self, obj):
        educations = obj.education_set.all()
        serializer = EducationSerializer(educations, many=True)
        return serializer.data
    
    def get_languages(self, obj):
        languages = obj.language_set.all()
        serializer = LanguageSerializer(languages, many=True)
        return serializer.data
    
    def get_portfolios(self, obj):
        portfolios = obj.portfolio_set.all()
        serializer = PortfolioSerializer(portfolios, many=True)
        return serializer.data
    
    def get_networkings(self, obj):
        networkings = obj.networking_set.all()
        serializer = NetworkingSerializer(networkings, many=True)
        return serializer.data
    
    def get_userrate(self, obj):
        userrate = UserRate.objects.filter(to_user=obj)
        serializer = UserRateSerializer(userrate, many=True)
        return serializer.data
    
    def get_useremploymenttype(self, obj):
        useremploymenttype = UserEmploymentType.objects.filter(user=obj)
        serializer = UserEmploymentTypeSerializer(useremploymenttype, many=True)
        return serializer.data
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if 'request' in self.context and instance.profile_picture:
            representation['profile_picture'] = self.context['request'].build_absolute_uri(instance.profile_picture.url)
        return representation
    

class MessageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Message
        fields = "__all__"

    sender = serializers.SerializerMethodField()
    recipient = serializers.SerializerMethodField()
    created = serializers.SerializerMethodField()

    def get_sender(self, obj):

        sender_id = obj.sender.id
        sender_email = obj.sender.user.email.lower()
        sender_name = obj.sender.user.name.lower()
        context = {
            "id": sender_id,
            "email": sender_email,
            "name": sender_name
        }
        return context
    
    def get_recipient(self, obj):

        recipient_id = obj.recipient.id
        recipient_email = obj.recipient.user.email.lower()
        recipient_name = obj.recipient.user.name.lower()
        context = {
            "id": recipient_id,
            "email": recipient_email,
            "name": recipient_name
        }
        return context
    
    def get_created(self, obj):
        date_time = str(obj.created).split(" ")
        date = date_time[0]
        time = date_time[1].split(".")[0]
        context = {
            "date": date,
            "time": time,
        }
        return context
    
class MessageDeletedSerializer(serializers.ModelSerializer):

    message = MessageSerializer()

    class Meta:
        model = MessageDeleted
        fields = "__all__"

    # def to_representation(self, obj):
    #     representation = super().to_representation(obj)
    #     representation['message'] = MessageSerializer(obj.message).data
    #     return representation


    
    

    
    