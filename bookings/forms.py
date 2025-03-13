from django import forms
from .models import Booking, SessionType, User


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Підтвердити пароль")

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'username', 'password']
        labels = {
        'first_name': "Ім'я",
        'last_name': 'Прізвище',
        'email': 'Електронна пошта',
        'phone_number': 'Телефон',
        'username': 'Логін',
        }

        def clean(self):
            cleaned_data = super().clean()
            password = cleaned_data.get("password")
            confirm_password = cleaned_data.get("confirm_password")

            if password and confirm_password and password != confirm_password:
                raise forms.ValidationError("Паролі не співпадають.")

            return cleaned_data


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

    def clean(self):
        cleaned_data = super().clean()
        service = cleaned_data.get('service')
        session_type = cleaned_data.get('session_type')
        if service and session_type and session_type.service != service:
            raise forms.ValidationError("Обраний тип заняття не належить до обраної послуги.")
        return cleaned_data