from rest_framework import serializers
from .models import Profile, Language, Skills, Experience, Education, Portfolio, ExpectedSalary, Networking, UserRate

class UserRateSerailizer(serializers.ModelSerializer):

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
        fields = ["skill_name", "skill_level"]

class LanguageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Language
        fields = ["language", "proficiency"]

class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = "__all__"

    skills = SkillsSerializer(many=True)
    languages = LanguageSerializer(many=True)
    experiences = serializers.SerializerMethodField()
    educations = serializers.SerializerMethodField()
    portfolios = serializers.SerializerMethodField()
    expectedsalary = ExpectedSalarySerializer(many=False)
    networkings = serializers.SerializerMethodField()
    userrate = serializers.SerializerMethodField()

    def get_experiences(self, obj):
        experiences = obj.experience_set.all()
        serializer = ExperienceSerializer(experiences, many=True)
        return serializer.data
    
    def get_educations(self, obj):
        educations = obj.education_set.all()
        serializer = EducationSerializer(educations, many=True)
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
        serializer = UserRateSerailizer(userrate, many=True)
        return serializer.data
    
    