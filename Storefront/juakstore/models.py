from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime
from django.db.models import Q

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
    company = models.CharField(max_length=30, verbose_name="Agency Name")
    info = models.CharField(max_length=200, verbose_name="Additional Info")
    name = models.CharField(max_length=30, verbose_name="Manager Name") 
    approved = models.BooleanField() 

    program = models.CharField(max_length=30, verbose_name="Program Name") 
    facilitator = models.CharField(max_length=30, verbose_name="Program Facilitator") 
    position = models.CharField(max_length=30, verbose_name="Position") 
    address = models.CharField(max_length=100)
    phones = models.CharField(max_length=80, verbose_name="Phone Numbers")
    faxes = models.CharField(max_length=80, verbose_name="Fax Numbers")
    email = models.EmailField()
    astatus = models.CharField(max_length=30, verbose_name="Agreement Status")
    istatus = models.CharField(max_length=30, verbose_name="Insurance Status")

    def __unicode__(self):
        return (self.uID)

class Booking(models.Model):
    name = models.CharField(max_length=200)
    notes = models.CharField(max_length=500)
    category = models.ForeignKey(BookingCategory)
    date = models.DateField()
    start = models.TimeField()
    end = models.TimeField()
    booker = models.ForeignKey(User)
    room = models.ForeignKey(Room)
    approved = models.BooleanField() 

    def is_active(self):
        return timezone.make_aware(datetime.combine(self.date, self.start),
                                   timezone.get_default_timezone()) \
               >= timezone.localtime(timezone.now())

    def __unicode__(self):
        return self.name


    '''
        Returns true if this booking conflicts with another booking
    '''
    def has_conflict(self):
        return self.get_conflicts().count() > 0

    '''
        Returns a queryset corresponding to the conflicting bookings
    '''
    def get_conflicts(self):
        overlap = Booking.objects.all().filter(
            ~Q(id__exact=self.id) & Q(room_id=self.room) & Q(date=self.date) &
            ((Q(start__gte=self.start) & Q(start__lt=self.end))
            | (Q(end__gt=self.start) & Q(end__lte=self.end))
            | (Q(start__lt=self.start) & Q(end__gt=self.end))
            | (Q(start__gt=self.start) & Q(end__lt=self.end))))
        return overlap
#
#class MultiRoomBooking(models.Model):
#    source = models.ForeignKey(Booking, related_name="multi_source")
#    target = models.ForeignKey(Booking, related_name="multi_target")

class RepeatBooking(models.Model):
    source = models.ForeignKey(Booking, related_name="repeat_source", on_delete=models.CASCADE)
    target = models.ForeignKey(Booking, related_name="repeat_target", on_delete=models.CASCADE)


def _getTargetBookingID(sourceSet):
    targetIDs = []
    for target in sourceSet.values('target'):
        targetIDs.append(target['target'])
    return targetIDs

'''
    Given a booking, returns a query set of all the related bookings
'''
def getRepeatBookings(booking):
    allBookings = Booking.objects.all()
    sourceSet = RepeatBooking.objects.all().filter(source_id=booking)
    if sourceSet.count() > 0: # this means that this was the first booking
        targetIDs = _getTargetBookingID(sourceSet)
        return allBookings.filter(id__in=targetIDs)
    else: # this means that it is an intermediate booking, need to find the original and all those related to it
        sourceID = RepeatBooking.objects.all().filter(target_id=booking).values('source')[0]['source']
        sourceSet = RepeatBooking.objects.all().filter(source_id=sourceID)
        targetIDs = _getTargetBookingID(sourceSet)
        targetIDs.append(sourceID)
        return allBookings.filter(id__in=targetIDs)





class ClientBooking(models.Model):
    start = models.DateTimeField('start')
    end = models.DateTimeField('end')
    client_name = models.CharField(max_length=20)
    client_email = models.EmailField()
    # NOTE: see when creating form: http://stackoverflow.com/questions/19130942/whats-the-best-way-to-store-phone-number-in-django-models
    phone_number = models.CharField(max_length=20)
    booking = models.ForeignKey(Booking)
