from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Client, Booking, Service, SessionType

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'phone', 'email']
        labels = {
            'name': 'Імʼя',
            'phone': 'Телефон',
            'email': 'Email',
        }

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['service', 'session_type', 'date', 'time']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }
        labels = {
            'service': 'Послуга',
            'session_type': 'Тип заняття',
            'date': 'Дата',
            'time': 'Час',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['session_type'].queryset = SessionType.objects.none()

        if 'service' in self.data:
            try:
                service_id = int(self.data.get('service'))
                self.fields['session_type'].queryset = SessionType.objects.filter(service_id=service_id)
            except (ValueError, TypeError):
                pass

    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date < timezone.now().date():
            raise ValidationError("Не можна обрати дату в минулому.")
        return date

    def clean_time(self):
        time = self.cleaned_data.get('time')
        date = self.cleaned_data.get('date')
        if date == timezone.now().date() and time < timezone.now().time():
            raise ValidationError("Не можна обрати час в минулому.")
        return time

    def clean(self):
        cleaned_data = super().clean()
        service = cleaned_data.get('service')
        session_type = cleaned_data.get('session_type')
        if service and session_type and session_type.service != service:
            raise ValidationError("Обраний тип заняття не належить до обраної послуги.")
        return cleaned_data