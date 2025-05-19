from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, Team

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name']
        
class ProfileSerializer(serializers.ModelSerializer):
    team = TeamSerializer()
    
    class Meta:
        model = Profile
        fields = ['team']

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'profile']