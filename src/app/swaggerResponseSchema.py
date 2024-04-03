from rest_framework import serializers

class CharityHelpsStatistics_ResponseSchema(serializers.Serializer):
    involvedPercent = serializers.IntegerField()
    totalPrice = serializers.IntegerField()

class GetAllUserHelpersCount_ResponseSchema(serializers.Serializer):
    totalHelpers = serializers.IntegerField()
    recent = serializers.ListField()

class otpLogin_ResponseSchema(serializers.Serializer):
    token = serializers.CharField(default="Bearer 'JWTtoken'")    

class otpLogin_Error_ResponseSchema(serializers.Serializer):
    message = serializers.CharField(default="کد یکبارمصرف و یا شماره تماس نادرست است")    

class Login_ResponseSchema(serializers.Serializer):
    otp = serializers.IntegerField(default=12345)

class Login_Error_ResponseSchema(serializers.Serializer):
    message = serializers.CharField(default="کاربری با این شماره یافت نشد.")

class UserDetails_ResponceSchema(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()
    firstName = serializers.CharField()
    lastName = serializers.CharField()
    profilePhoto = serializers.CharField(default="image path")
    totalMonths = serializers.IntegerField()
    expiration = serializers.IntegerField()
    totalPrice = serializers.IntegerField()


class UserDetails_Error_ResponceSchema(serializers.Serializer):
    detail = serializers.CharField(default="اطلاعات برای اعتبارسنجی ارسال نشده است.")

class AddHelp_Success_ResponceSchema(serializers.Serializer):
    message = serializers.CharField(default="شما با موفقیت در این پروژه شریک شدید.")

class AddHelp_Locked_ResponceSchema(serializers.Serializer):
    message = serializers.CharField(default="شما قبلاً در این پروژه مشارکت کرده‌اید.")

class AddHelp_BadRequest_ResponceSchema(serializers.Serializer):
    message = serializers.CharField(default='خطایی هنگام پردازش درخواست شما رخ داد')

class DeleteHelp_NoContent_ResponceSchema(serializers.Serializer):
    message = serializers.CharField(default="اشتراک شما با موفقیت لغو شد.")

class DeleteHelp_UnAuthorized_ResponceSchema(serializers.Serializer):
    message = serializers.CharField(default='کاربری با مشخصات مشخص شده یافت')

class DeleteHelp_NotFound_ResponceSchema(serializers.Serializer):
    message = serializers.CharField(default='اشتراکی با این شناسه وجود ندارد')

class UpdateHelp_NotFound_ResponceSchema(serializers.Serializer):
    message = serializers.CharField(default="No CharityHelp with id : 0  Excist !!!")

class Project_NotFound_ResponceSchema(serializers.Serializer):
    message = serializers.CharField(default='پروژه‌ای با این شناسه یافت نشد')