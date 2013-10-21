from django.views import generic
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.template import RequestContext, loader
from django.contrib.auth.models import User
from models import Booking, BookingCategory, Room
from forms import BookingForm

@login_required
def index(request):
    template = loader.get_template('juakstore/index.html')
    all_bookings = Booking.objects.all()
    context = RequestContext(request, {
        'all_bookings': all_bookings
    })
    return HttpResponse(template.render(context))

def addBooking(request):
    if request.method == "POST":
        f = BookingForm(request.POST)
        if f.is_valid():
            newBooking = Booking(name=request.POST['name'],
                          notes=request.POST['notes'],
                          date=request.POST['date'],
                          start=request.POST['start'],
                          end=request.POST['end'],
                          booker=get_object_or_404(User, pk=request.POST['booker']),
                          category=get_object_or_404(BookingCategory, pk=request.POST['category']),
                          room=get_object_or_404(Room, pk=request.POST['room']))
            newBooking.save()
            return HttpResponseRedirect(reverse('juakstore:bookingDetail', args=(newBooking.id,)))
        else:
            return render(request, 'juakstore/booking_add.html', {'form': f})
    else:
        return HttpResponseRedirect(reverse('juakstore:bookingCreate'))

def updateBooking(request, pk):
    #start = request.POST['event_start']
    #end = request.POST['event_end']
    #if end < start:
    #    return render(request, {'form': request.POST, 'error': 'End time must be after start time'})
    #else:
    if request.method == "POST":
        b = get_object_or_404(Booking, pk=pk)
        f = BookingForm(request.POST)
        if f.is_valid():
            b.name = request.POST['name']
            b.notes = request.POST['notes']
            b.start = request.POST['start']
            b.end = request.POST['end']
            b.category = get_object_or_404(BookingCategory, pk=request.POST['category'])
            b.room = get_object_or_404(Room, pk=request.POST['room'])
            b.save()
            return HttpResponseRedirect(reverse('juakstore:bookingDetail', args=(b.id,)))
        else:
            return render(request, 'juakstore/booking_update.html', {'form': f, 'booking': b})
    else:
        form = BookingForm()
        return HttpResponseRedirect(reverse('juakstore:bookingDetail', args=(pk,)))

def displayBooking(request, pk):
    b = get_object_or_404(Booking, pk=pk)
    return render(request, 'juakstore/bookingdetail.html', {'booking':b})

class BookingView(generic.DetailView):
    model = Booking
    template_name = 'juakstore/bookingdetail.html'

class BookingCreate(generic.edit.CreateView):
    model = Booking
    template_name = 'juakstore/booking_add.html'
    form_class = BookingForm

class BookingUpdate(generic.edit.UpdateView):
    model = Booking
    template_name = 'juakstore/booking_update.html'
    form_class = BookingForm

class UserDetailView(generic.DetailView):
    model = User
    template_name = 'juakstore/user.html'