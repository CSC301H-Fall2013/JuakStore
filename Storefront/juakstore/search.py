__author__ = 'MISSCATLADY'

import datetime
from django.shortcuts import render
#from django.forms.models import modelformset_factory
#from django.shortcuts import render_to_response
from django.http import HttpResponse
from juakstore.models import Room, BookingCategory, Partner, Booking



def search_booking(request):
	errors = []
	if 'q' in request.GET:
		q = request.GET['q']
		if not q:
			errors.append("Enter a room to search.")
		else:
			rooms = Room.objects.filter(name__icontains=q)
			return render(request, 'juakstore/SEARCH.html', 
				{'rooms': rooms, 'query': q})

	return render(request, 'juakstore/SEARCH.html', {'errors' : errors})



