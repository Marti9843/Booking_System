from django import forms
from .models import Client, Booking, Service, SessionType

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'phone', 'email']

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['service', 'session_type', 'date', 'time']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['session_type'].queryset = SessionType.objects.none()

        if 'service' in self.data:
            try:
                service_id = int(self.data.get('service'))
                self.fields['session_type'].queryset = SessionType.objects.filter(service_id=service_id)
            except (ValueError, TypeError):
                pass
