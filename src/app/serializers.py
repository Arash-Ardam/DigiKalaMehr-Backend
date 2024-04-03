from rest_framework import serializers
from app.models import *

class OtpLoginSerializer(serializers.Serializer):
    otp = serializers.CharField()
    phone = serializers.CharField()

class UserAuthenticateSerializer(serializers.Serializer):
    phone = serializers.CharField()
    
class AllCharityInfoDto(serializers.Serializer):
    totalHelpUsers = serializers.IntegerField()
    recentHelpers = serializers.CharField()
    
class AddCharityHelpDTO(serializers.Serializer):
    projectId = serializers.IntegerField()
    price = serializers.IntegerField()
    
class UpdateCharityHelpDTO(serializers.Serializer):
    projectId = serializers.IntegerField()
    price = serializers.IntegerField()
    
class HelpDTO(serializers.ModelSerializer):
    class Meta:
        model = CharityHelp
        fields = "__all__"
        
class DeleteHelpDTO(serializers.Serializer):
    helpId = serializers.IntegerField()
    

class InstituteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institute
        fields = "__all__"
        
class ProjectDTO(serializers.ModelSerializer):
    institute = InstituteSerializer()
    class Meta:
        model = Project
        fields = "__all__"
     
class UserDTO(serializers.ModelSerializer):
    class Meta:
        model = MehrUser
        exclude = ("password","is_active","is_superuser","is_verified","groups","last_login","user_permissions","is_staff")

class CharityHelpDTO(serializers.ModelSerializer):
    project = ProjectDTO()
    user = UserDTO()
    class Meta:
        model = CharityHelp
        fields = "__all__"

class ExtendHelpDto(serializers.Serializer):
    helpId = serializers.IntegerField() 
    
class ResponseHelpDTO(serializers.ModelSerializer):
    project = ProjectDTO()
    class Meta:
        model = CharityHelp
        exclude = ("is_enabled","user")
    
        
    