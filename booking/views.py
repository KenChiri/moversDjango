from django.shortcuts import render,redirect
from booking.forms import *

def book_service(request):
    if request.method == 'POST':
        form = ServiceBookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()
            send_mail(
                'Service Booking Confirmation',
                'Your service booking request has been received.',
                'from@example.com',
                [request.user.email],
                fail_silently=False,
            )
            return redirect('home')
    else:
        form = ServiceBookingForm()
    return render(request, 'book_service.html', {'form': form})
