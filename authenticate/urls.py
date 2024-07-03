from django.contrib import admin
from django.urls import path, include 
from . import views

urlpatterns = [
    path('signup', views.signup, name='signup'),
    path('login', views.user_login, name='login'), 
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('logout', views.user_logout, name='logout'),
    path('index', views.index, name='index'),
    path('password-reset/<uidb64>/<token>', views.pwdReset, name='password-reset'),
    path('verifyMail', views.mail_otp, name='verifyMail'),
]

