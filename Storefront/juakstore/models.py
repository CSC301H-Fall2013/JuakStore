from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime

# Create your models here.

class Room(models.Model):
    name = models.CharField(max_length=20)
    info = models.CharField(max_length=500)


    def __unicode__(self):
        return self.name

class BookingCategory(models.Model):
    name = models.CharField(max_length=40)

    def __unicode__(self):
        return self.name

class Partner(models.Model):
    uID = models.ForeignKey(User)
    company = models.CharField(max_length=30)
    info = models.CharField(max_length=500)
    name = models.CharField(max_length=30)
    approved = models.BooleanField()

class Booking(models.Model):
    name = models.CharField(max_length=200)
    notes = models.CharField(max_length=500)
    category = models.ForeignKey(BookingCategory)
    date = models.DateField()
    start = models.TimeField()
    end = models.TimeField()
    booker = models.ForeignKey(User)
    room = models.ForeignKey(Room)

    def is_active(self):
        return datetime.combine(self.date, self.end) >= timezone.now()

    def __unicode__(self):
        return self.name

class ClientBooking(models.Model):
    start = models.DateTimeField('start')
    end = models.DateTimeField('end')
    client_name = models.CharField(max_length=20)
    client_email = models.EmailField()
    # NOTE: see when creating form: http://stackoverflow.com/questions/19130942/whats-the-best-way-to-store-phone-number-in-django-models
    phone_number = models.CharField(max_length=20)
    booking = models.ForeignKey(Booking)