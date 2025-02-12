from django.urls import path
from . import views

urlpatterns = [
    path('book/', views.booking_view, name='booking'),
    path('success/', views.booking_success, name='booking_success'),
    path('get-session-types/', views.get_session_types, name='get_session_types'),
]