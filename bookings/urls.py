from django.urls import path
from . import views

urlpatterns = [
    path('', views.service_booking, name='service_booking'),
    path('success/', views.success, name='success'),
]
