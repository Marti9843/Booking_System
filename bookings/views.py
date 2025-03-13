from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import logout as auth_logout, login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Service, SessionType, Booking, Users
from .forms import BookingForm, CustomUserCreationForm

# Головна сторінка запису на послугу
@login_required
def booking_view(request):
    if request.method == 'POST':
        booking_form = BookingForm(request.POST)
        if booking_form.is_valid():
            booking = booking_form.save(commit=False)
            booking.user = request.user  # Зв'язуємо запис з поточним користувачем
            booking.save()
            messages.success(request, 'Запис успішно створено!')
            return redirect('booking_success')
    else:
        booking_form = BookingForm()

    return render(request, 'bookings/booking.html', {
        'booking_form': booking_form,
        'services': Service.objects.all(),
    })

# Отримання типів занять для обраної послуги (AJAX)
def get_session_types(request):
    service_id = request.GET.get('service_id')
    session_types = SessionType.objects.filter(service_id=service_id)
    data = [{'id': st.id, 'name': st.get_session_type_display()} for st in session_types]
    return JsonResponse(data, safe=False)

# Сторінка успішного запису
def booking_success(request):
    return render(request, 'bookings/booking_success.html')

# Сторінка "Про нас"
def about(request):
    return render(request, 'bookings/about.html')

# Сторінка "Новини"
def news(request):
    return render(request, 'bookings/news.html')

# Реєстрація користувача
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)  # Автоматично увійти після реєстрації
            messages.success(request, 'Реєстрація успішна! Ласкаво просимо.')
            return redirect('about')  # Перенаправити на сторінку "Про нас"
    else:
        form = CustomUserCreationForm()
    return render(request, 'bookings/register.html', {'form': form})

# Вхід у систему
def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)  # Увійти в систему
            messages.success(request, f'Вітаємо, {user.username}!')
            return redirect('about')  # Перенаправити на головну сторінку
    else:
        form = AuthenticationForm()
    return render(request, 'bookings/login.html', {'form': form})

# Вихід з системи
def custom_logout(request):
    auth_logout(request)  # Вийти з системи
    messages.success(request, 'Ви успішно вийшли з акаунту.')
    return redirect('about')  # Перенаправити на сторінку "Про нас"