from django.shortcuts import render, redirect
from .models import Service, Client, Booking
from .forms import ClientForm, BookingForm

def service_booking(request):
    services = Service.objects.all()

    if request.method == 'POST':
        client_form = ClientForm(request.POST)
        booking_form = BookingForm(request.POST)

        if client_form.is_valid() and booking_form.is_valid():
            client = client_form.save()
            booking = booking_form.save(commit=False)
            booking.client = client
            booking.save()
            return redirect('success')  # Після успішного запису переходимо на сторінку підтвердження

    else:
        client_form = ClientForm()
        booking_form = BookingForm()

    return render(request, 'bookings/service_booking.html', {
        'services': services,
        'client_form': client_form,
        'booking_form': booking_form
    })

def success(request):
    return render(request, 'bookings/success.html')
