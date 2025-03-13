from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from .models import Users, Booking, Service, SessionType

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

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(max_length=30, required=True, label="Логін")
    first_name = forms.CharField(max_length=30, required=True, label="Ім'я")
    last_name = forms.CharField(max_length=30, required=True, label="Прізвище")
    phonenumber = forms.CharField(
        max_length=20,
        required=True,
        label="Номер телефону",
        validators=[RegexValidator(r'^\+?1?\d{9,15}$', "Номер телефону повинен бути у форматі: '+380XXXXXXXXX'.")]
    )
    email = forms.EmailField(required=True, label="Електронна пошта")

    class Meta:
        model = Users  # Використовуємо кастомну модель Users
        fields = ("username", "first_name", "last_name", "phonenumber", "email", "password1", "password2")

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if Users.objects.filter(username=username).exists():
            raise ValidationError("Користувач з таким логіном вже існує.")
        return username

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 7:
            raise ValidationError("Пароль повинен містити щонайменше 7 символів.")
        return password1