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
from dateutil.relativedelta import *


class SummaryForm(forms.Form):
    category = forms.ModelMultipleChoiceField(required=False, queryset=BookingCategory.objects.all())
    partner = forms.ModelMultipleChoiceField(required=False, queryset=Partner.objects.all())
    room = forms.ModelMultipleChoiceField(required=False, queryset=Room.objects.all())
    start_date = forms.DateField(label="Start Date", widget=SelectDateWidget)
    end_date = forms.DateField(label="End Date", widget=SelectDateWidget)

def search_category(request):
    errors = []
    notfirst = False
    if request.method == 'POST':
        form = SummaryForm(request.POST)
        if form.is_valid():
            notfirst = True
            room = form.cleaned_data['room']
            partner = form.cleaned_data['partner']
            category = form.cleaned_data['category']
            sd = form.cleaned_data['start_date']
            ed = form.cleaned_data['end_date']

            if sd > ed:
                errors.append("Please make sure your start date is before your end date.")
                return render(request, 'juakstore/summary.html', {'form': form, 'errors': errors})
            else:
            #filter days
                low_bound = Booking.objects.filter(date__gte=sd)
                upper_bound = Booking.objects.filter(date__lte=ed)
                TOTAL = (low_bound & upper_bound)

            #filter rooms
            tmp = Room.objects.none()
            if room:
                for r in room:
                    tmp = (tmp | TOTAL.filter(room__exact=r))
                TOTAL_rooms = tmp

            #filter partner
            tmp = Room.objects.none()
            if partner:
                for p in partner:
                    tmp = (tmp | TOTAL.filter(booker__exact=p))
                TOTAL = tmp

            #filter category
            tmp = Room.objects.none()
            if category:
                for c in category:
                    tmp = (tmp | TOTAL.filter(category__exact=c))
                TOTAL = tmp

            BOOKINGS = tmp.count()
            TIME = get_hrs(TOTAL)

            return render(request, 'juakstore/summary.html', {'form': form,
                'category': category, 'room': room, 'notfirst': notfirst, 'partner':partner,
                'sd':sd, 'ed': ed, 'TOTAL': TOTAL, 'TIME':TIME, 'BOOKINGS':BOOKINGS,
                'errors':errors  })
        else:
            return render(request, 'juakstore/summary.html', {'form': form})
    else:
        form = SummaryForm()
        return render(request, 'juakstore/summary.html', {'form': form})

#Returns total hours in bookings_list
def get_hrs(bookings_list):
    time = relativedelta(datetime.now(), datetime.now()).hours
    for b in bookings_list:
        time = time + relativedelta(datetime.combine(date.today(), b.end),
         datetime.combine(date.today(), b.start)).hours
    return time


class SearchForm(forms.Form):
    date = forms.DateField(label="Date", widget=SelectDateWidget)
    start = forms.TimeField(widget=SelectTimeWidget(twelve_hr=True, minute_step=10))
    end = forms.TimeField(widget=SelectTimeWidget(twelve_hr=True, minute_step=10))

    def clean(self):
        cleaned_data = super(SearchForm, self).clean()
        if cleaned_data.get('start') >= cleaned_data.get('end'):
            raise ValidationError('Start time must be after end time')
        return cleaned_data

def search_form(request):
    if request.method == 'POST':
        f = SearchForm(request.POST)
        if f.is_valid():
            available_rooms = Room.objects.all()
            date = f.cleaned_data['date']
            start = f.cleaned_data['start']
            end = f.cleaned_data['end']
            conflicts = Booking.objects.all().filter(Q(date=date) &
                ((Q(start__gte=start) & Q(start__lt=end))
                | (Q(end__gt=start) & Q(end__lte=end))
                | (Q(start__lt=start) & Q(end__gt=end))
                | (Q(start__gt=start) & Q(end__lt=end))))
            if conflicts.count > 0:
                conflictRoomIDs = []
                for c in conflicts.values('room'):
                    conflictRoomIDs.append(c['room'])
                available_rooms = available_rooms.exclude(id__in=conflictRoomIDs)
            print available_rooms
            return render(request, 'juakstore/search.html', {'form':SearchForm(),
                                                             'availableRooms': available_rooms,
                                                             'date': f.cleaned_data['date'],
                                                             'start': f.cleaned_data['start'],
                                                             'end': f.cleaned_data['end'],
                                                             'submitted': True})
        else:
            return render(request, 'juakstore/search.html', {'form': f})
    else:
        form = SearchForm()
        return render(request, 'juakstore/search.html', {'form': form})

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

