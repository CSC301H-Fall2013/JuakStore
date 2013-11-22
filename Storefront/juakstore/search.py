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
    category = forms.ModelMultipleChoiceField(required=False, queryset=BookingCategory.objects.all())
    partner = forms.ModelMultipleChoiceField(required=False, queryset=Partner.objects.all())
    room = forms.ModelMultipleChoiceField(required=False, queryset=Room.objects.all())
    start_date = forms.DateField(label="Start Date", widget=SelectDateWidget)
    end_date = forms.DateField(label="End Date", widget=SelectDateWidget)

def search_category(request):
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

            return render(request, 'juakstore/search_category.html', {'form': form,
                'category': category, 'room': room, 'notfirst': notfirst, 'partner':partner,
                'sd':sd, 'ed': ed, 'TOTAL': TOTAL, 'TIME':TIME, 'BOOKINGS':BOOKINGS,
                'errors':errors  })
        else:
            return render(request, 'juakstore/search_category.html', {'form': form})
    else:
        form = SEARCHFORM()
        return render(request, 'juakstore/search_category.html', {'form': form})

#Returns total hours in bookings_list
def get_hrs(bookings_list):
    time = relativedelta(datetime.now(), datetime.now()).hours
    for b in bookings_list:
        time = time + relativedelta(datetime.combine(date.today(), b.end),
         datetime.combine(date.today(), b.start)).hours
    return time


class SearchForm(forms.Form):
    DAYS = ((2,'Mon'), (3, 'Tues'), (4, 'Wed'), (5, 'Thur'), 
    (6, 'Fri'), (7, 'Sat'), (1, 'Sun'))
    room = forms.ModelMultipleChoiceField(queryset=Room.objects.all())
    start_date = forms.DateField(label="Start Date", widget=SelectDateWidget)
    end_date = forms.DateField(label="End Date", widget=SelectDateWidget)
    days = forms.MultipleChoiceField(label="Days", widget=forms.CheckboxSelectMultiple, choices=DAYS)
    start_time = forms.TimeField(label="Start Time", widget=SelectTimeWidget(minute_step=10))
    end_time = forms.TimeField(label="End Time", widget=SelectTimeWidget(minute_step=10))

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
                errors.append("Please make sure your start time is before your end time.")
                return render(request, 'juakstore/SEARCH_LIA.html', {'form': form, 'errors': errors})

            if sd >= ed:
                errors.append("Please make sure your start date is before your end date.")
                return render(request, 'juakstore/SEARCH_LIA.html', {'form': form, 'errors': errors})
            
            COMMON_MONTHS = [(1, 'Jan'), (2, 'Feb'), (3, 'Mar'), (4, 'Apr'), (5, 'May'),
            (6, 'Jun'), (7, 'Jul'), (8, 'Aug'), (9, 'Sept'), (10, 'Oct'), (11, 'Nov'), (12, 'Dec')]

            DATE = relativedelta(ed, sd)
            TIME = relativedelta(datetime.combine(date.today(), et), datetime.combine(date.today(), st))
            DATE_list=list()
            TIME_list=list()
            for i in range(0, DATE.months):
                if i + 1 <= ed.month:
                    DATE_list.append(COMMON_MONTHS[sd.month + i - 1])
            for i in range(0, TIME.hours):
                if i + 1 > datetime.combine(date.today(), et).hour:
                    TIME_list.append(i + 1)


            #need new vars for actual results
            #filter days
            low_bound = Booking.objects.filter(date__gte=sd)
            upper_bound = Booking.objects.filter(date__lte=ed)
            RDates = (low_bound & upper_bound)

            RTimes = Room.objects.none()
            for d in RDates:
                RTimes = (low_bound.filter(start__gte=st) & upper_bound.filter(end__lte=et))

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
                           'end_date': ed, 'DATE': DATE_list, 'TIME': TIME_list,
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

