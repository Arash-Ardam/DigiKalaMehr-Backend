from django.contrib.auth.models import BaseUserManager


class AuthUserManager(BaseUserManager):
    def create_user(self , username , phone,**extra_fields):
        user = self.model(username = username , phone = phone,**extra_fields)
        user.set_password(extra_fields['password'])
        user.save(using = self._db)
        return user
    
    def create_superuser(self , username , phone , **extra_fields):
     

        user = self.create_user(username , phone,**extra_fields)
        user.is_staff = True
        user.is_admin = True
        user.is_active =  True
        user.is_superuser = True
        user.save(using = self._db)
        return user

        