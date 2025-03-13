from django.contrib import admin
from .models import Service, SessionType, Booking

# Реєструємо моделі
admin.site.register(Service)
admin.site.register(SessionType)
admin.site.register(Booking)
