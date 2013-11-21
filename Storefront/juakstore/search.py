__author__ = 'MISSCATLADY'

import datetime
from models import *
from widgets import SelectTimeWidget
from django import forms
from django.shortcuts import render
from django.http import HttpResponse
from django.forms.extras.widgets import SelectDateWidget
from django.http import HttpResponse, HttpResponseRedirect
from datetime import *
from dateutil.relativedelta import *


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room


class SearchForm(forms.Form):
    DAYS = ((2,'Mon'), (3, 'Tues'), (4, 'Wed'), (5, 'Thur'), 
    	(6, 'Fri'), (7, 'Sat'), (1, 'Sun'))
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
            room = form.cleaned_data['room']
            sd = form.cleaned_data['start_date']
            ed = form.cleaned_data['end_date']
            st = form.cleaned_data['start_time']
            et = form.cleaned_data['end_time']
            days = form.cleaned_data['days']
             


            if st > et:
                errors.append["Please make sure your start time is before your end time."]
                return render(request, 'juakstore/SEARCH_LIA.html', {'form': form, 'errors': errors})

            if sd >= ed:
                errors.append["Please make sure your start date is before your end date."]
                return render(request, 'juakstore/SEARCH_LIA.html', {'form': form, 'errors': errors})
            DATE = relativedelta(ed, sd)
            TIME = relativedelta(datetime.combine(date.today(), et), datetime.combine(date.today(), st))
                


            #need new vars for actual results
            #filter days
            low_bound = Booking.objects.filter(date__gte=sd)
            upper_bound = Booking.objects.filter(date__lte=ed)
            RDates = (low_bound & upper_bound)

            RTimes = ()
            for d in RDates:
            	RTimes = (low_bound.filter(start__gte=st) 
            		& upper_bound.filter(end__lte=et))

            RT_tmp = Room.objects.none()
            for d in days:
                RT_tmp = (RT_tmp | RTimes.filter(date__week_day=d))

            RTimes = RT_tmp 

            RT_tmp2 = Room.objects.none()
            for r in room:
                RT_tmp2 = (RT_tmp2 | RTimes.filter(room__exact=r)) 

            RTimes = RT_tmp2 #all the booked times




            return render(request, 'juakstore/SEARCH_LIA.html',
                          {'room': room,
                           'start_date': sd, 'booked': RTimes,
                           'end_date': ed, 'DATE': DATE, 'TIME': TIME,
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

