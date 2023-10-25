from rest_framework import serializers
from .models import Profile, Language, Skills

class SkillsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Skills
        fields = "__all__"

class LanguageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Language
        fields = "__all__"

class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = "__all__"

    skills = SkillsSerializer(many=True)
    languages = LanguageSerializer(many=True)

class LanguageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Language
        fields = "__all__"

    user = ProfileSerializer(many=True)
    