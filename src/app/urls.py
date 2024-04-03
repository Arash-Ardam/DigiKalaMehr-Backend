from django.urls import path
from . import views
from . import LoginAPIs
from django.conf import settings
from datetime import datetime


urlpatterns = [
# path('getTotalHelps/<user>', views.getTotalHelps,name='totalHelp'),
path('auth/otp/', LoginAPIs.Login, name = 'PhoneLogin'),
path('auth/login/', LoginAPIs.otpLogin, name = 'OtpLogin'),

path('getTotalMonthsExpiration/',views.getTotalMonthsExpiration,name = 'getTotalMonthsExpiration'),

path('projects/',views.AllProjects,name = 'AllProjects'),
path('projects/<projectId>/', views.SingleProject, name = 'SingleProject'),

path('me/details/', LoginAPIs.UserDetails, name = "userDetails"),
path('me/projects/', LoginAPIs.AllProjectsForUser, name = 'AllProjectsForUser'),

path('me/helps/create', views.AddHelp, name = 'AddHelp'),
path('me/helps/', views.getUserHelpHistory, name = "getUserHelpHistory"),
path('me/helps/active/', views.getActiveHelps, name = 'getActiveHelps'),
path('me/helps/<helpId>/delete/', views.DeleteHelp, name = 'DeleteHelp'),
path('me/helps/<helpId>/edit/', views.UpdateHelp, name = 'UpdateHelp'),
path('me/helps/<helpId>/extend/', views.extendHelp, name='extendHelp'),

path('analytics/users/', views.GetAllUserHelpersCount, name = 'totalHelps'),
path('analytics/projects/',views.CharityHelpsStatistics, name = 'CharityHelpsStatistics'),
]