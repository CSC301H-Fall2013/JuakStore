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
    	('Fri', 'Fri'), ('Six', 'Sat'), ('Sat', 'Sun'))
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

            return render(request, 'juakstore/SEARCH_LIA.html',
                          {'room': room,
                           'start_date': sd, 
                           'end_date': ed, 
                           'start_time': st, 'end_time': et,
                           'form': form, 'notfirst': notfirst, 'days': days})
        else:
            return render(request, 'juakstore/SEARCH_LIA.html', {'form': form})

        '''if not request.POST.get('room',''):
            errors.append('Enter a room.')
        #why does start_date split up into these?! friggin django
        sd = request.POST.get('start_date_day', '')
        sm = request.POST.get('start_date_month', '')
        sy = request.POST.get('start_date_year', '')
        if not sd and not sm and not sy:
            errors.append('Enter a start date.')
        ed = request.POST.get('end_date_day', '')
        em = request.POST.get('end_date_month', '')
        ey = request.POST.get('end_date_year', '')
        if not ed and em and ey:
            errors.append('Enter an end date.')
        if not request.POST.get('days', ''):
            erros.append('Please check a day of the week.')
        if not request.POST.get('start_time', ''):
            errors.append('Enter a start time.')
        if not request.POST.get('end_time', ''):
            errors.append('Enter a end time.')
        if not errors:
            return render(request, 'juakstore/SEARCH_LIA.html',
        #only gets last room WHY?! how turn back to query set?
        {'room': form.cleaned_data['room'] ,
        'start_date_day': sd, 'start_date_month': sm, 'start_date_year': sy,
        'end_date_day': ed, 'end_date_month': em, 'end_date_year': ey,
        'start_time': request.POST.get('start_time', ''), 'end_time': request.POST.get('end_time', ''),
        'form': form, 'notfirst': notfirst, 'days': days})'''
    else:
        form = SearchForm()
        return render(request, 'juakstore/SEARCH_LIA.html', {'form': form})
        #return render(request, 'juakstore/SEARCH_LIA.html', {'errors': errors, 'notfirst': notfirst, 'form': form})

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

