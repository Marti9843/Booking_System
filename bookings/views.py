from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Service, SessionType
from .forms import ClientForm, BookingForm

def booking_view(request):
    if request.method == 'POST':
        client_form = ClientForm(request.POST)
        booking_form = BookingForm(request.POST)
        if client_form.is_valid() and booking_form.is_valid():
            client = client_form.save()
            booking = booking_form.save(commit=False)
            booking.client = client
            booking.save()
            return redirect('booking_success')
    else:
        client_form = ClientForm()
        booking_form = BookingForm()

    return render(request, 'bookings/booking.html', {
        'client_form': client_form,
        'booking_form': booking_form,
        'services': Service.objects.all(),
    })

def get_session_types(request):
    service_id = request.GET.get('service_id')
    session_types = SessionType.objects.filter(service_id=service_id)
    data = [{'id': st.id, 'name': st.get_session_type_display()} for st in session_types]
    return JsonResponse(data, safe=False)

def booking_success(request):
    return render(request, 'bookings/booking_success.html')