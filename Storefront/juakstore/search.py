__author__ = 'MISSCATLADY'

import datetime
from django.shortcuts import render
from django.http import HttpResponse
from models import *


def search_booking(request):
	errors = []
	if 'q' in request.GET:
		q = request.GET['q']
		if not q:
			errors.append("Enter a room to search.")
		else:
			rooms = Room.objects.filter(name__icontains=q)
			return render(request, 'bookingApp/search.html', 
				{'rooms': rooms, 'query': q})

	return render(request, 'bookingApp/search.html', {'errors' : errors})


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