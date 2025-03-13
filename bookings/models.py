from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models


class UserAccountManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        email = email.lower()

        user = self.model(
            email=email,
            **kwargs,
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **kwargs):
        user = self.create_user(
            email,
            password=password,
            **kwargs,
        )

        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, max_length=255)
    phone_number = models.CharField(max_length=255)
    username = models.CharField(max_length=255)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'phone_number']

    def __str__(self) -> str:
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


class Booking(models.Model):
    client = models.ForeignKey(User, related_name='bookings', on_delete=models.CASCADE)
    service = models.ForeignKey(Service, related_name='bookings', on_delete=models.CASCADE)
    session_type = models.ForeignKey(SessionType, related_name='bookings', on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return f"{self.client.username} - {self.service} на {self.date} о {self.time}"
