from urllib import response
from django.db.models import *
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import is_valid_path
from django.core.exceptions import MultipleObjectsReturned
from rest_framework.permissions import IsAuthenticated
from app.TokenHandler import JWTAuthenticateUser

from app.models import *
from rest_framework import *
from rest_framework import status
from rest_framework.decorators import *
from rest_framework.response import Response
from app.serializers import *
from drf_yasg.utils import swagger_auto_schema
from .swaggerResponseSchema import *



def get_error_response(message, status):
    return Response({ "message": message }, status)
# Create your views here.

# @api_view(['GET'])
# def getTotalHelps(request):
#     price = CharityHelp.objects.filter().aggregate(price = Count('score'))
#     return Response()

@swagger_auto_schema(
    method='post',
    request_body=UserAuthenticateSerializer,
    operation_summary= "لاگین کاربر با شماره تماس"
    )
@api_view(['POST'])
def AuthenticateUser(request):
    # authdetails = userAuthorizeSerializer(data= request.data)   

    userDto = UserAuthenticateSerializer(data=request.data)
    if userDto.is_valid():
        responseUser = MehrUser.objects.filter(phone = userDto.initial_data['phone']).values()
        userToken = JWTAuthenticateUser().Authenticate(request)
        if userToken == None:
            resultBody = {"user" : "no user" , "phone" : userDto.initial_data['phone']}
            # result = {"Status Code" : status.HTTP_400_BAD_REQUEST,"Body" : resultBody}
            return Response(resultBody,status = status.HTTP_400_BAD_REQUEST)
        
        help_history = CharityHelp.objects.filter(user =responseUser[0]['id']).order_by("-date").values()
        totalhelps = 0
        for x in help_history:
            totalhelps += x['price']
           
            pass
        help_history2 = CharityHelp.objects.filter(user =responseUser[0]['id']).order_by("-date")
        
        responseDTO = {"user":responseUser,"token" : f"Bearer {userToken}","totalhelpsPrice":totalhelps,"Help_History":CharityHelpDTO(help_history2,many = True).data,}
        
        # result = {"Status Code" : status.HTTP_200_OK,"Body" : responseDTO}
        return Response(responseDTO)
    
@swagger_auto_schema(
    method='get',
    responses={
        status.HTTP_200_OK : GetAllUserHelpersCount_ResponseSchema,
    },
    operation_summary= "نمایش تعداد کل کمک های انجام شده و 6 نفر اخیر شرکت کنندگان"
    )
@api_view(['GET'])
def GetAllUserHelpersCount(request):
    recentHelps = CharityHelp.objects.filter(state=State.paynext).order_by("-date").distinct()
    recentHelpsDTO  = CharityHelpDTO(recentHelps,many = True).data
    userListFullName = list()
    for x in recentHelpsDTO:
        FullName = "{0} {1}".format(x["user"]["firstName"],x["user"]["lastName"])
        userListFullName.append(FullName)
    helpersCount = CharityHelp.objects.all().values("user").distinct()   
    
    responseDto = {"totalHelpers" : helpersCount.count() , "recent" : userListFullName }

    return Response(responseDto)

@swagger_auto_schema(
    method='post',
    request_body=AddCharityHelpDTO,
    responses={
        '201':AddHelp_Success_ResponceSchema,
        '423':AddHelp_Locked_ResponceSchema,
        '400':AddHelp_BadRequest_ResponceSchema
    },
    operation_summary= "اضافه کردن کمک جدید"
    )
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def AddHelp(request):
    requestDTO = AddCharityHelpDTO(data = request.data)   
   
    if requestDTO.is_valid():
        user = JWTAuthenticateUser.GetUserFromToken(request)
        project = get_object_or_404(Project, id = requestDTO.initial_data['projectId'])
        price = requestDTO.initial_data['price']
        
        excistingCharityHelpCount = CharityHelp.objects.filter(price = price , user = user , project = project).count()
        if excistingCharityHelpCount != 0 :
            return get_error_response('شما قبلاً در این پروژه مشارکت کرده‌اید.', status=status.HTTP_423_LOCKED)
        
    if project and user is not None :
        newHelp = CharityHelp()
        newHelp.project = project
        newHelp.user = user
        newHelp.price = price
        newHelp.save()
        return Response({ "message": "شما با موفقیت در این پروژه شریک شدید."} , status=status.HTTP_201_CREATED)
    
    return get_error_response('خطایی هنگام پردازش درخواست شما رخ داد', status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='GET',
    responses={
        '200' : CharityHelpDTO(many = True),
        '401' : UserDetails_Error_ResponceSchema
    },
    operation_summary='نمایش تاریخچه کمک کاربر'
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getUserHelpHistory(request):
    user = JWTAuthenticateUser.GetUserFromToken(request)
    help_history =ResponseHelpDTO(CharityHelp.objects.filter(user = user).order_by("-date"),many =True)
    return Response(help_history.data)

@swagger_auto_schema(
    method='put',
    request_body=UpdateCharityHelpDTO,
    responses={
        '200' : UpdateCharityHelpDTO,
        '404' : UpdateHelp_NotFound_ResponceSchema,
        '401' : UserDetails_Error_ResponceSchema
    },
    operation_summary= "ویرایش کمک انتخاب شده"
)
@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def UpdateHelp(request,helpId):
    requestDTO = UpdateCharityHelpDTO(data= request.data)
    if requestDTO.is_valid():
        try:
            entity = CharityHelp.objects.get(id = helpId)
            updatedHelp = CharityHelp.objects.get(id = helpId)
            updatedHelp.project =  get_object_or_404(Project, id = requestDTO.initial_data['projectId'])
            updatedHelp.price = requestDTO.initial_data['price']
            updatedHelp.save()
            responseDTO = CharityHelpDTO(updatedHelp)
            return Response(responseDTO.data)

        except CharityHelp.DoesNotExist:
            return Response("No CharityHelp with id :{0}  Excist !!!".format(helpId),status=status.HTTP_404_NOT_FOUND)    


@swagger_auto_schema(
    method='delete',
    responses={
        '204' : DeleteHelp_NoContent_ResponceSchema,
        '404' : DeleteHelp_NotFound_ResponceSchema,
        '401' : DeleteHelp_UnAuthorized_ResponceSchema
    },
    operation_summary= "لغو یک کمک"
)
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def DeleteHelp(request,helpId):
    responseDTO = None
    authUser = JWTAuthenticateUser.GetUserFromToken(request)
    
    if authUser is None:
        return get_error_response('کاربری با مشخصات مشخص شده یافت', status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        responseDTO = CharityHelp.objects.get(id = helpId ,user =  authUser)
        responseDTO.delete()
        return HttpResponse({ "message": "اشتراک شما با موفقیت لغو شد." }, status=status.HTTP_204_NO_CONTENT)
    except CharityHelp.DoesNotExist:
        return get_error_response('اشتراکی با این شناسه وجود ندارد', status=status.HTTP_404_NOT_FOUND)

      
@swagger_auto_schema(
    method='get',
     responses={
        '200' : ProjectDTO(many = True),
    },
    operation_summary= "نمایش تمامی پروژه های موجود برای کمک "
    )
@api_view(["GET"])
def AllProjects(request):
    entity = Project.objects.all()
    responseDTO = ProjectDTO(entity,many=True)

    return Response(responseDTO.data) 


@swagger_auto_schema(
    method='get',
     responses={
        '200' : ProjectDTO,
        '404' : Project_NotFound_ResponceSchema
    },
    operation_summary= "نمایش یک پروژه بر اساس آیدی آن"
    )
@api_view(["GET"])
def SingleProject(request, projectId):
    try:
        entity = Project.objects.get(id=projectId)
        responseDTO = ProjectDTO(entity, many=False)
        
        return Response(responseDTO.data)       
    except Project.DoesNotExist:
        return get_error_response('پروژه‌ای با این شناسه یافت نشد', status=status.HTTP_404_NOT_FOUND)


@swagger_auto_schema(
    method='get',
    responses={
        status.HTTP_200_OK: CharityHelpsStatistics_ResponseSchema
    },
    operation_summary= "نمایش درصد شرکت کنندگان در پروژه ها و مجموع مبلغ های کمک شده"
    )
@api_view(["GET"])
def CharityHelpsStatistics(request):
    allHelps = CharityHelp.objects.filter(state=State.success).values_list('price',flat=True)
    alluserCount = MehrUser.objects.count()
    usersInHelpCount = CharityHelp.objects.values_list('user',flat=True).distinct().count()
    totalPrice = 0
    for x in allHelps:
        totalPrice += x
        pass
    invalvedUsersPercent = usersInHelpCount / alluserCount * 100
    
    responseDTO = {"involvedPercent": round(invalvedUsersPercent,0) , "totalPrice": totalPrice}

    return Response(responseDTO)   


@swagger_auto_schema(
    method='get',
    operation_summary= 'نمایش تعداد ماه ها و مدت انقضا'
)
@api_view(["GET"])    
@permission_classes([IsAuthenticated])
def getTotalMonthsExpiration(request):
    user = JWTAuthenticateUser.GetUserFromToken(request)
    totalMonths = None
    try:
        userhelps = []
        for item in CharityHelp.objects.filter(user = user).order_by('date') :
            userhelps.append(item)
        
    
        totalMonths = JWTAuthenticateUser.diff_month(userhelps[-1].date,userhelps[0].date)
    
        expiration = userhelps[-1].expiration
        context = {"totalMonths" : totalMonths, "expiration" : expiration}
        return Response(context)
    except IndexError:
        return get_error_response("پروژه فعالی برای این کاربر یافت نشد",status.HTTP_404_NOT_FOUND)


@swagger_auto_schema(
    method='post',
    responses={
        '200' : "successfully extended !!!"
    },
    operation_summary= 'تمدید کمک کاربر'
)    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def extendHelp(request,helpId):
    # extendDto = ExtendHelpDto(data = request.data)
    user = JWTAuthenticateUser.GetUserFromToken(request)
    expiredHelp = CharityHelp.objects.get(id = helpId,user=user,state=State.expired)
    expiredHelp.state = State.paynext
    expiredHelp.expiration = 6
    expiredHelp.save()
    return HttpResponse("successfully extended !!!")


@swagger_auto_schema(
    method='get',
    responses={
        '200' : CharityHelpDTO,
        '401' : UserDetails_Error_ResponceSchema
    },
    operation_summary= 'نمایش پروژه های فعال کاربر'
)    
@api_view(['GET'])
@permission_classes([IsAuthenticated])     
def getActiveHelps(request):
    user = JWTAuthenticateUser.GetUserFromToken(request)
    try:
        activeHelps = CharityHelp.objects.get(Q(user=user) & ~Q(state = State.success))
        responseDto = ResponseHelpDTO(activeHelps,many=False)

        return Response(responseDto.data)
    except CharityHelp.DoesNotExist:
        return get_error_response("پروژه فعالی برای این کاربر موجود نیست",status.HTTP_404_NOT_FOUND)
    except MultipleObjectsReturned:
        multipleActiveHelps = CharityHelp.objects.filter(Q(user=user) & ~Q(state = State.success)).order_by("-date")
        multipleActiveHelps[0].delete()
        return get_error_response("امکان فعال بودن چند پروژه فعال برای کاربر موجود نیست", status=status.HTTP_400_BAD_REQUEST)    