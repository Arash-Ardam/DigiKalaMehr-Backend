from django.contrib.auth.backends import BaseBackend, ModelBackend
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404



class AuthBackend(BaseBackend):
    def authenticate(self, authPhone=None,**kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(phone = authPhone)
            return user
        except UserModel.DoesNotExist:
            return None
       

        
        


    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None