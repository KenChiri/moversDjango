from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views
from django.contrib import admin

app_name = 'moverhome'
urlpatterns = [
    path('community/', views.community, name='community'),
    path('support/', views.support, name='support'),
    path('contact/', views.contactus, name='contact'),
    path('about/', views.aboutus, name='about'),
    path('', views.homepage, name='home'),
    path('bookings',include('booking.urls')),
]