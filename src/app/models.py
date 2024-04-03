from datetime import datetime , timedelta
from persiantools.jdatetime import JalaliDate
from django.db import models
from django.utils.translation import activate
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .AuthUserManager import AuthUserManager



class OtpUser(models.Model):
    otp = models.IntegerField(max_length=5, default=12345)
    user = models.ForeignKey('MehrUser', on_delete=models.DO_NOTHING)


class MehrUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=20)  # possible digikala database users
    firstName = models.CharField(max_length=50, null=True, blank=True)
    lastName = models.CharField(max_length=50, null=True, blank=True)
    profilePhoto = models.ImageField(upload_to='admin-interface/images', height_field=None, width_field=None, max_length=None,
                                     null=True, blank=True)
    phone = models.CharField(max_length=11, unique=True)  # possible digikala database users

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ["username", "firstName", "lastName"]

    objects = AuthUserManager()

    def __str__(self):
        fullname = "{0} {1}".format(self.firstName, self.lastName)
        return fullname
    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"    


class Project(models.Model):
    institute = models.ForeignKey('Institute', on_delete=models.CASCADE)
    description = models.CharField(max_length=500)
    topic = models.CharField(max_length=20)
    logo = models.ImageField(upload_to='admin-interface/project_logos', blank=True, null=True)

    def __str__(self):
        return self.topic
    class Meta:
        verbose_name = "پروژه"
        verbose_name_plural = "پروژه ها"    


class Institute(models.Model):
    name = models.CharField(max_length=50)
    logo = models.ImageField(upload_to='admin-interface/institute_logos')

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "موسسه"
        verbose_name_plural = "موسسه ها"
    


class State(models.TextChoices):  # will be extended
    paynext = 'next', _('پرداخت بعدی')
    success = 'success', _('موفق')
    expired = 'expired' , _('انقضا شده')


class CharityHelp(models.Model):
    LANGUAGES = (
        ('fa', 'Persian'),
        ('en', 'English'),
    )
    activate('fa')
    
    
    user = models.ForeignKey(MehrUser, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    price = models.IntegerField()

    month_name = _(JalaliDate.today().strftime("%B"))
    year_name = _(JalaliDate.today().strftime("%Y"))
    subject = _("{month} {year}").format(month=month_name, year=year_name)

    date = models.DateField(default=datetime.now())
    state = models.CharField(max_length=20, choices=State.choices, default=State.paynext)


    # total_months = models.IntegerField(default=months)
    expiration = models.IntegerField(default=6)
    is_enabled = models.BooleanField(default=False)

    def __str__(self):
        description = "{0} توسط {1} ({2})".format(self.project, self.user, _(self.state))
        return description
    

    class Meta:
        verbose_name = "کمک"
        verbose_name_plural = "کمک ها"    
