from django.shortcuts import render
from booking.views import *
# Create your views here.
def homepage(request):
    return render(request, 'moverhome/home.html')
def community(request):
    return render(request, 'community.html')
def aboutus(request):
    return render(request, 'about.html')
def support(request):
    return render(request, 'support.html')
def contactus(request):
    return render(request, 'contact.html')