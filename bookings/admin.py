from django.contrib import admin
from .models import Service, SessionType, Client, Booking

# Реєструємо моделі
admin.site.register(Service)
admin.site.register(SessionType)
admin.site.register(Client)
admin.site.register(Booking)
