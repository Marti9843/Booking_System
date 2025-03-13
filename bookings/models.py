from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

class Users(AbstractUser):
    # Додаткові поля
    phonenumber = models.CharField(
        max_length=15,
        unique=True,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$', "Номер телефону повинен бути у форматі: '+380XXXXXXXXX'.")],
        verbose_name="Номер телефону"
    )
    email = models.EmailField(unique=True, verbose_name="Електронна пошта")

    # Додаткові налаштування
    USERNAME_FIELD = 'email'  # Використовуємо email для входу
    REQUIRED_FIELDS = ['username', 'phonenumber']  # Обов'язкові поля при створенні користувача

    def __str__(self):
        return self.email
class Service(models.Model):
    FITNESS = 'fitness'
    POOL = 'pool'
    YOGA = 'yoga'
    MASSAGE = 'massage'

    SERVICE_CHOICES = [
        (FITNESS, 'Фітнес-зал'),
        (POOL, 'Басейн'),
        (YOGA, 'Йога'),
        (MASSAGE, 'Масаж'),
    ]

    name = models.CharField(max_length=100, choices=SERVICE_CHOICES, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.get_name_display()

class SessionType(models.Model):
    GROUP = 'group'
    INDIVIDUAL = 'individual'

    SESSION_CHOICES = [
        (GROUP, 'Групове'),
        (INDIVIDUAL, 'Індивідуальне'),
    ]

    service = models.ForeignKey(Service, related_name='session_types', on_delete=models.CASCADE)
    session_type = models.CharField(max_length=20, choices=SESSION_CHOICES)

    def __str__(self):
        return f"{self.service} - {self.get_session_type_display()}"

    def __str__(self):
        return self.name

class Booking(models.Model):
    client = models.ForeignKey(Users, related_name='bookings', on_delete=models.CASCADE)
    service = models.ForeignKey(Service, related_name='bookings', on_delete=models.CASCADE)
    session_type = models.ForeignKey(SessionType, related_name='bookings', on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return f"{self.client.name} - {self.service} на {self.date} о {self.time}"