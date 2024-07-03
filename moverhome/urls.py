from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views
from django.contrib import admin

app_name = 'moverhome'
urlpatterns = [
    path('home', views.homepage, name='home'),
]