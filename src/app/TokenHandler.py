from random import randint
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from app.models import *
from rest_framework import status

# from src.app.models import AuthUser

from app.serializers import *
from .CustomAuthentication import AuthBackend
from rest_framework_simplejwt.tokens import RefreshToken , AccessToken
from django.contrib.auth import get_user_model


class JWTAuthenticateUser():
    @classmethod
    def UserAuthenticate(self,request):
        userDto = UserAuthenticateSerializer(data=request.data)
        authUser = authenticate(userDto.initial_data["phone"])

        if authUser is None:
            return None
            
        otp = randint(10000,99999)
        OtpUser.objects.create(otp = otp, user = authUser)

        context = { "otp": otp }
        return context
    
    @classmethod
    def GetUserFromToken(self,request):
        UserModel = get_user_model()

        try:
            headerToken = request.headers["Authorization"][7:]
            userToken =AccessToken(headerToken)
            user = UserModel.objects.get(id = userToken['user_id'])
            return user
        except UserModel.DoesNotExist:
            return None
        
    @classmethod
    def OtpAuthenticate(self,request):
        otpDto = OtpLoginSerializer(data=request.data)
        
        try:
            otp = otpDto.initial_data["otp"]
            phone = otpDto.initial_data["phone"]

            otpUser = OtpUser.objects.get(otp=otp)

            if otpUser.user.phone != phone:
                return None
            
            token = RefreshToken.for_user(otpUser.user)
            otpUser.delete()
            return token.access_token
        except OtpUser.DoesNotExist:
            return None

    @classmethod
    def getAllProjectsForUser(self,request):   
        try : 
            user = JWTAuthenticateUser.GetUserFromToken(request)
            helpProject = CharityHelp.objects.get(state=State.paynext , user=user)
            helpProjectsDto =CharityHelpDTO(helpProject)

            entity = Project.objects.exclude(id = helpProject.project.id)
            responseDTO = ProjectDTO(entity,many=True)
            return responseDTO.data
        except CharityHelp.DoesNotExist:    
            entity = Project.objects.all()
            responseDTO = ProjectDTO(entity,many=True)
            return responseDTO.data

    @classmethod
    def diff_month(self,d1, d2):
        return (d1.year - d2.year) * 12 + d1.month - d2.month            

        
        

    