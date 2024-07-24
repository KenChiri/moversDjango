from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views
from django.contrib import admin
urlpatterns = [
 path('book/', views.book_service, name='book_service')]