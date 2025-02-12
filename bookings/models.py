from django.db import models


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


class Client(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name


class Booking(models.Model):
    client = models.ForeignKey(Client, related_name='bookings', on_delete=models.CASCADE)
    service = models.ForeignKey(Service, related_name='bookings', on_delete=models.CASCADE)
    session_type = models.ForeignKey(SessionType, related_name='bookings', on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return f"{self.client.name} - {self.service} на {self.date} о {self.time}"
