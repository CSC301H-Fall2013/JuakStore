__author__ = 'MISSCATLADY'

import datetime
from django import forms
from django.shortcuts import render
from django.http import HttpResponse
from models import *
from django.forms.extras.widgets import SelectDateWidget


class RoomForm(forms.ModelForm):
	class Meta:
		model = Room

class SearchForm(forms.Form):

	room = forms.ModelMultipleChoiceField(queryset=Room.objects.all())
	start_date = forms.DateField(label="Start Date", widget=SelectDateWidget)
	end_date = forms.DateField(label="End Date", widget=SelectDateWidget)

def search_form(request):
	errors = []
	notfirst = False
	form = SearchForm(request.POST)
	if request.method == 'POST':
		notfirst = True
		if not request.POST.get('room',''):
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
		if not errors:
			return render(request, 'juakstore/SEARCH.html',
	 	#only gets last room WHY?! how turn back to query set?
        {'room': request.POST.get('room','') , 
        'start_date_day': sd, 'start_date_month': sm, 'start_date_year': sy,
        'end_date_day': ed, 'end_date_month': em, 'end_date_year': ey,
        'form': form, 'notfirst': notfirst})

	return render(request, 'juakstore/SEARCH.html',
        {'errors': errors,
        'form': form, 'notfirst': notfirst})


# Search available rooms with given date and time period.
# Return list of Room objects.
def search_available_rooms(date, start_time, end_time):

	all_rooms = Room.objects.all()
	booked_rooms = Room.objects.filter(booking__date=date)
	unavailable_rooms_one = booked_rooms.filter(booking__start__gte=start_time).filter(booking__start__lt=end_time)
	unavailable_rooms_two = booked_rooms.filter(booking__end__lte=end_time).filter(booking__start__gt=start_time)

	return all_rooms - unavailable_rooms_one - unavailable_rooms_two

# Search available rooms with given date, time period and room type.
# Return list of Room objects.
def search_available_rooms_with_type(date, start_time, end_time, room_type):
	all_rooms = Room.objects.all().filter(type=room_type)
	booked_rooms = Room.objects.filter(booking__date=date)
	unavailable_rooms_one = booked_rooms.filter(booking__start__gte=start_time).filter(booking__start__lt=end_time)
	unavailable_rooms_two = booked_rooms.filter(booking__end__lte=end_time).filter(booking__start__gt=start_time)

	return all_rooms - unavailable_rooms_one - unavailable_rooms_two

