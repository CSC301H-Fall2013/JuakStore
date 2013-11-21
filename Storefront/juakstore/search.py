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


class CategoryForm(forms.ModelForm):
    class Meta:
        model = BookingCategory

class PartnerForm(forms.ModelForm):
    class Meta:
        model = Partner

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room

class SEARCHFORM(forms.Form):
    category = forms.ModelMultipleChoiceField(queryset=BookingCategory.objects.all())
    partner = forms.ModelMultipleChoiceField(queryset=Partner.objects.all())
    room = forms.ModelMultipleChoiceField(queryset=Room.objects.all())
    start_date = forms.DateField(label="Start Date", widget=SelectDateWidget)
    end_date = forms.DateField(label="End Date", widget=SelectDateWidget)

def search_cat(request):
    errors = []
    notfirst = False
    if request.method == 'POST':
        form = SEARCHFORM(request.POST)
        if form.is_valid():
            notfirst = True
            room = form.cleaned_data['room']
            partner = form.cleaned_data['partner']
            category = form.cleaned_data['category']
            sd = form.cleaned_data['start_date']
            ed = form.cleaned_data['end_date']

            #filter days
            low_bound = Booking.objects.filter(date__gte=sd)
            upper_bound = Booking.objects.filter(date__lte=ed)
            TOTAL = (low_bound & upper_bound)

            #filter rooms
            tmp = Room.objects.none()
            for r in room:
                tmp = (tmp | TOTAL.filter(room__exact=r))
            #filter partner
            TOTAL = tmp
            tmp = Room.objects.none()
            for p in partner:
                tmp = (tmp | TOTAL.filter(booker__exact=p.uID))
            #filter category
            TOTAL = tmp
            tmp = Room.objects.none()
            for c in category:
                tmp = (tmp | TOTAL.filter(category__exact=c))

            TOTAL = tmp

            return render(request, 'juakstore/search_category.html', {'form': form,
                'category': category, 'room': room, 'notfirst': notfirst,
                'sd':sd, 'ed': ed })
        else:
            return render(request, 'juakstore/search_category.html', {'form': form})
    else:
        form = SEARCHFORM()
        return render(request, 'juakstore/search_category.html', {'form': form})


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

