__author__ = 'MISSCATLADY'

import datetime
from models import *
from widgets import SelectTimeWidget
from django import forms
from django.shortcuts import render
from django.http import HttpResponse
from django.forms.extras.widgets import SelectDateWidget
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ValidationError
from datetime import *


class search_booking_form(forms.Form):
    category = forms.ModelMultipleChoiceField(required=False, queryset=BookingCategory.objects.all())
    partner = forms.ModelMultipleChoiceField(required=False, queryset=Partner.objects.all())
    room = forms.ModelMultipleChoiceField(required=False, queryset=Room.objects.all())
    start_date = forms.DateField(label="Start Date", widget=SelectDateWidget)
    end_date = forms.DateField(label="End Date", widget=SelectDateWidget)

def search_booking(request):
    errors = []
    notfirst = False
    if request.method == 'POST':
        notfirst = True
        form = search_booking_form(request.POST)
        if form.is_valid():
            room = form.cleaned_data['room']
            partner = form.cleaned_data['partner']
            category = form.cleaned_data['category']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']

            if start_date > end_date:
                errors.append("Please make sure your start date is before your end date.")
                return render(request, 'juakstore/search_booking.html', {'form': form, 'errors': errors})
            else:
            # filter by date
                bookings = Booking.objects.filter(date__gte=start_date).filter(date__lte=end_date)

            # filter by room
            if room:
                keys = []
                for r in room:
                    keys.append(r.pk)
                bookings.filter(room__pk__in=keys)

            # filter by partner
            if partner:
                keys = []
                for p in partner:
                    keys.append(p.pk)
                bookings.filter(partner__pk__in=keys)

            #filter by category
            if category:
                for c in category:
                    keys.append(c.pk)
                bookings.filter(category__pk__in=keys)

            td = get_bookings_time(bookings)
            time = ' hours '.join(str(td).split(':')[:2]) + ' minutes'
            count = bookings.count()

            return render(request, 'juakstore/search_booking.html', {'form': form,
                'category': category, 'room': room, 'partner':partner,
                'start_date':start_date, 'end_date': end_date, 'count': count, 'time':time, 'bookings':bookings,
                'errors':errors, 'notfirst':notfirst })
        else:
            return render(request, 'juakstore/search_booking.html', {'form': form})
    else:
        form = search_booking_form()
        return render(request, 'juakstore/search_booking.html', {'form': form})

#Return total hours in list bookings.
def get_bookings_time(bookings):
    time = timedelta()
    for booking in bookings:
            length = booking.end - booking.start
            time = time + length
    return time


class search_available_room_form(forms.Form):
    date = forms.DateField(label="Date", widget=SelectDateWidget)
    start_time = forms.TimeField(label="Start Time", widget=SelectTimeWidget(twelve_hr=True, minute_step=10))
    end_time = forms.TimeField(label="End Time", widget=SelectTimeWidget(twelve_hr=True, minute_step=10))


# Search available rooms with given date and time period.
# Return list of Room objects.
def search_available_room(request):
    errors = []
    notfirst = False
    if request.method == 'POST':
        notfirst = True
        form = search_available_room_form(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            start_time = form.cleaned_data['start_time']
            end_time = form.cleaned_data['end_time']

            if start_time >= end_time:
                errors.append("Please make sure your start time is before your end time.")
                return render(request, 'juakstore/search_room.html', {'form': form, 'errors': errors})
            else:
                all_rooms = list(Room.objects.all())
                booked_rooms = Room.objects.filter(booking__date=date)
                unavailable_rooms_one = list(booked_rooms.filter(booking__start__gte=start_time).filter(booking__start__lt=end_time))
                unavailable_rooms_two = list(booked_rooms.filter(booking__end__lte=end_time).filter(booking__start__gt=start_time))
                available_rooms = all_rooms - unavailable_rooms_one - unavailable_rooms_two
                count = available_rooms.count()

            return render(request, 'juakstore/search_room.html', {'form': form,
                'rooms': available_rooms, 'date':date , 'start_time':start_time, 'end_time': end_time, 'count': count,
                'errors':errors, 'notfirst':notfirst })
        else:
            return render(request, 'juakstore/search_room.html', {'form': form})
    else:
        form = search_available_room_form()
        return render(request, 'juakstore/search_room.html', {'form': form})


# Calculate total time booked per partner.
# Return dictionary mapping Partner object to timedelta object.
def get_time_per_partner():
    time_per_partnder = {}
    for p in Partner.objects.all():
        bookings = Booking.objects.filter(booker_id__exact=p.uID)
        time = timedelta()
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
        time = timedelta()
        for booking in bookings:
            length = booking.end - booking.start
            time = time + length
        time_per_category[ca] = time

    return time_per_category

