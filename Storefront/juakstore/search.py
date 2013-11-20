__author__ = 'MISSCATLADY'

import datetime
from models import *
from widgets import SelectTimeWidget
from django import forms
from django.shortcuts import render
from django.http import HttpResponse
from django.forms.extras.widgets import SelectDateWidget
from django.http import HttpResponse, HttpResponseRedirect


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room


class SearchForm(forms.Form):
    DAYS = (('Mon','Mon'), ('Tues', 'Tues'), ('Wed', 'Wed'), ('Thur', 'Thur'), 
    	('Fri', 'Fri'), ('Sat', 'Sat'), ('Sun', 'Sun'))
    room = forms.ModelMultipleChoiceField(queryset=Room.objects.all())
    start_date = forms.DateField(label="Start Date", widget=SelectDateWidget)
    end_date = forms.DateField(label="End Date", widget=SelectDateWidget)
    days = forms.MultipleChoiceField(label="Days", widget=forms.CheckboxSelectMultiple, choices=DAYS)
    start_time = forms.TimeField(label="Start Time", widget=SelectTimeWidget(twelve_hr=True, minute_step=10))
    end_time = forms.TimeField(label="End Time", widget=SelectTimeWidget(twelve_hr=True, minute_step=10))


def search_form(request):
    errors = []
    notfirst = False
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            notfirst = True
            errors.append("HERE")
            room = form.cleaned_data['room']
            sd = form.cleaned_data['start_date']
            ed = form.cleaned_data['end_date']
            st = form.cleaned_data['start_time']
            et = form.cleaned_data['end_time']
            days = form.cleaned_data['days']

            #need new vars for actual results
            #filter days
            low_bound = Booking.objects.filter(date__gte=sd)
            upper_bound = Booking.objects.filter(date__lte=ed)
            RDates = list(low_bound & upper_bound)

            RTimes = ()
            for d in RDates:
            	RTimes = list(low_bound.filter(start__gte=st) 
            		& upper_bound.filter(end__lte=et))


            return render(request, 'juakstore/SEARCH_LIA.html',
                          {'room': room,
                           'start_date': sd, 'booked': RTimes,
                           'end_date': ed, 
                           'start_time': st, 'end_time': et,
                           'form': form, 'notfirst': notfirst, 'days': days})
        else:
            return render(request, 'juakstore/SEARCH_LIA.html', {'form': form})
    else:
        form = SearchForm()
        return render(request, 'juakstore/SEARCH_LIA.html', {'form': form})

# Search available rooms with given date and time period.
# Return list of Room objects.
def search_available_rooms(date, start_time, end_time):
    all_rooms = list(Room.objects.all())
    booked_rooms = Room.objects.filter(booking__date=date)
    unavailable_rooms_one = list(
        booked_rooms.filter(booking__start__gte=start_time).filter(booking__start__lt=end_time))
    unavailable_rooms_two = list(booked_rooms.filter(booking__end__lte=end_time).filter(booking__start__gt=start_time))

    return all_rooms - unavailable_rooms_one - unavailable_rooms_two

# Calculate total time booked per partner.
# Return dictionary mapping Partner object to timedelta object.
def get_time_per_partner():
    time_per_partnder = {}
    for p in Partner.objects.all():
        bookings = Booking.objects.filter(booker_id__exact=p.uID)
        time = timedelta(0)
        for booking in bookings:
            length = booking.end - booking.start
            time = time + length
        time_per_partner[p] = time

    return time_per_partner


# Calculate total time booked per category.
# Return dictionary mapping BookingCategory object to timedelta object.
def get_time_per_booking_category():
    time_per_category = {}
    for ca in BookingCategory.objects.all():
        bookings = Booking.objects.filter(category_id__exact=ca.id)
        time = timedelta(0)
        for booking in bookings:
            length = booking.end - booking.start
            time = time + length
        time_per_category[ca] = time

    return time_per_category

