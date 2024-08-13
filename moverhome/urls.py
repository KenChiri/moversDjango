from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views
from django.contrib import admin

app_name = 'moverhome'
urlpatterns = [
    path('', views.community, name='community'),
    path('', views.support, name='support'),
    path('', views.contactus, name='contact'),
    path('', views.aboutus, name='about'),
    path('', views.homepage, name='home'),
    path('',include('booking.urls')),
]