from django.db import models
from datetime import date
from time import time

# Create your models here.
MAX_NUMBER_OF_SEATS = 6
MAX_LEN_NAME = 50

class Table(models.Model):
    SEATS_PER_TABLE = [(i, str(i)) for i in range(2, MAX_NUMBER_OF_SEATS+1, 2)]

    class TableStatus(models.TextChoices):
        AVAILABLE = 'available'
        UNAVAILABLE = 'unavailable'

    seats = models.IntegerField(choices=SEATS_PER_TABLE)
    status = models.CharField(max_length=20, choices=TableStatus.choices, default='available')


# One table can have different dates
class TableDate(models.Model):
    name = models.CharField(max_length=MAX_LEN_NAME)
    date = models.DateField(null=True, blank=True)
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name='dates')



class Customer(models.Model):
    MAX_LEN_PHONE = 13
    GUEST_CHOICES = [(i, str(i)) for i in range(0, MAX_NUMBER_OF_SEATS+1)]

    name = models.CharField(max_length=MAX_LEN_NAME)
    phone_number = models.CharField(max_length=MAX_LEN_PHONE)
    number_of_guests = models.IntegerField(choices=GUEST_CHOICES)
    date = models.DateField(default=date.today, null=True, blank=True)
    time = models.TimeField(default=time, null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
   
    table = models.ForeignKey(Table, on_delete=models.SET_NULL, null=True, blank=True)

