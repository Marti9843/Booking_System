from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Головна сторінка запису на послугу
    path('book/', views.booking_view, name='booking'),

    # Сторінка успішного запису
    path('success/', views.booking_success, name='booking_success'),

    # Отримання типів занять для обраної послуги (AJAX)
    path('get-session-types/', views.get_session_types, name='get_session_types'),

    # Сторінка "Про нас"
    path('about/', views.about, name='about'),

    # Сторінка "Новини"
    path('news/', views.news, name='news'),

    # Реєстрація користувача
    path('register/', views.register, name='register'),

    # Авторизація користувача
    path('login/', auth_views.LoginView.as_view(template_name='bookings/login.html'), name='login'),

    # Вихід з акаунту
    path('logout/', views.custom_logout, name='logout'),
]