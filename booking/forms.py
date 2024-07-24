from django import forms
from django.contrib.auth.models import User
from .models import ServiceBooking
class ServiceBookingForm(forms.ModelForm):
    class Meta:
        model = ServiceBooking
        fields = ['service_type', 'source_location', 'destination_location']
