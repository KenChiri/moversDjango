from django.shortcuts import render
from booking.views import *
# Create your views here.
def homepage(request):
    return render(request, 'moverhome/home.html')