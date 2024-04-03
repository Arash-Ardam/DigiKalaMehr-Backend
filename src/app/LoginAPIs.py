

from random import randint
from django.contrib.auth import authenticate
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from app.TokenHandler import JWTAuthenticateUser
from app.models import CharityHelp

from app.serializers import *
from app.ResponseHandler import BuildResponse
from .swaggerResponseSchema import *


def get_error_response(message, status):
    return Response({ "message": message }, status)

@swagger_auto_schema(
    method='post',
    request_body=UserAuthenticateSerializer,
    responses={
        '200' : Login_ResponseSchema,
        '404' : Login_Error_ResponseSchema
    },
    operation_summary= "لاگین کاربر با شماره تماس"
    )
@api_view(["POST"])
def Login(request):
    UserAuthentication = JWTAuthenticateUser.UserAuthenticate(request)
    if UserAuthentication != None:
        return Response(UserAuthentication)
    else:
        return get_error_response('کاربری با این شماره یافت نشد.', status=status.HTTP_404_NOT_FOUND)
    
@swagger_auto_schema(
    method='post',
    request_body=OtpLoginSerializer,
    responses={
        '200' : otpLogin_ResponseSchema,
        '400' : otpLogin_Error_ResponseSchema
    },
    operation_summary= "لاگین کاربر با شماره otp"
    )
@api_view(["POST"])
def otpLogin(request):
    authenticateOtp = JWTAuthenticateUser.OtpAuthenticate(request)    
    
    if authenticateOtp != None:
        context = {"token" : f"Bearer {authenticateOtp}"}
        return Response(context)
    else:
        return get_error_response('کد یکبارمصرف و یا شماره تماس نادرست است', status=status.HTTP_400_BAD_REQUEST)

        
@swagger_auto_schema(
    method='get',
    responses={
        '200': UserDetails_ResponceSchema,
        '401': UserDetails_Error_ResponceSchema,
    },
    operation_summary= "دریافت اطلاعات کاربر صحت سنجی شده با سابقه کمک ها"
    )
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def UserDetails(request):
    user = JWTAuthenticateUser.GetUserFromToken(request)
    if user == None :
        return get_error_response(message='کاربری با این اطلاعات یافت نشد', status=status.HTTP_404_NOT_FOUND)

    try:
        totalMonths = None
        totalPrice = 0
        userhelps = []
        for item in CharityHelp.objects.filter(user = user).order_by('date') :
            if item.state == State.success:
                totalPrice += item.price
            userhelps.append(item)
        
    
        totalMonths = JWTAuthenticateUser.diff_month(userhelps[-1].date,userhelps[0].date)
    
        expiration = userhelps[-1].expiration    

        userResponse = BuildResponse.ForUser(user,totalMonths,expiration,totalPrice)
        return Response(userResponse)
    except IndexError:
        userResponse = BuildResponse.ForUser(user,0,0,0)
        return Response(userResponse)

@swagger_auto_schema(
    method='get',
    responses={
        '200' : ProjectDTO(many = True),
        '401' : UserDetails_Error_ResponceSchema
    },
    operation_summary= "نمایش تمامی پروژه های موجود برای کمک کاربر"
    )
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def AllProjectsForUser(request):
    context = JWTAuthenticateUser.getAllProjectsForUser(request)
    return Response(context)    

