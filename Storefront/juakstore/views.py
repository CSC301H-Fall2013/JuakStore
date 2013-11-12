from django.views import generic
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext, loader
from django.contrib.auth.models import User
from models import Booking, BookingCategory, Room
from forms import BookingForm, RoomForm
from mycalendar import BookingCalendar
from django.utils.safestring import mark_safe
import datetime

@login_required
def index(request, year=None, month=None, day=None):
    if year:
        year = int(year)
    else:
        year = datetime.datetime.now().year
    if month:
        month = int(month)
    else:
        month = datetime.datetime.now().month
    if day:
        day = int(day)
    else:
        day = datetime.datetime.now().day

    template = loader.get_template('juakstore/index.html')
    newBooking = BookingForm()
    all_bookings = Booking.objects.all()
    all_rooms = Room.objects.all()
    context = RequestContext(request, {
        'all_bookings': all_bookings,
        'all_rooms': all_rooms,
        'year': year,
        'month': month,
        'day': day,
        'form': newBooking
    })
    return HttpResponse(template.render(context))

def addBooking(request):
    if request.method == "POST":
        f = BookingForm(request.POST)
        if f.is_valid():
            newBooking = Booking(name=f.cleaned_data['name'],
                          notes=f.cleaned_data['notes'],
                          date=f.cleaned_data['date'],
                          start=f.cleaned_data['start'],
                          end=f.cleaned_data['end'],
                          booker=get_object_or_404(User, pk=request.POST['booker']),
                          category=get_object_or_404(BookingCategory, pk=request.POST['category']),
                          room=get_object_or_404(Room, pk=request.POST['room']))
            newBooking.save()
            return HttpResponseRedirect(reverse('juakstore:bookingDetail', args=(newBooking.id,)))
        else:
            return render(request, 'juakstore/booking_add.html', {'form': f})
    else:
        return HttpResponseRedirect(reverse('juakstore:bookingCreate'))

def calendar(request, year, month):
    foundBookings = Booking.objects.order_by(date__year=year, date__month=month)
    cal  = BookingCalendar(foundBookings).formatmonth(year, month)
    return render_to_response('index.html', {'calendar':mark_safe(cal),})

def updateBooking(request, pk):
    #start = request.POST['event_start']
    #end = request.POST['event_end']
    #if end < start:
    #    return render(request, {'form': request.POST, 'error': 'End time must be after start time'})
    #else:
    if request.method == "POST":
        b = get_object_or_404(Booking, pk=pk)
        f = BookingForm(request.POST)
        f.id = pk

        if f.is_valid():
            b.name = f.cleaned_data['name']
            b.notes = f.cleaned_data['notes']
            b.start = f.cleaned_data['start']
            b.end = f.cleaned_data['end']
            b.category = get_object_or_404(BookingCategory, pk=f.cleaned_data['category'].id)
            b.room = get_object_or_404(Room, pk=f.cleaned_data['room'].id)
            b.save()
            return HttpResponseRedirect(reverse('juakstore:bookingDetail', args=(b.id,)))
        else:
            return render(request, 'juakstore/booking_update.html', {'form': f, 'booking': b})
    else:
        form = BookingForm()
        return HttpResponseRedirect(reverse('juakstore:bookingDetail', args=(pk,)))

def submitRoom(request):
    if request.method == "POST":
        f = RoomForm(request.POST)
        if f.is_valid():
            newRoom = Room(name=request.POST['name'], info=request.POST['info'])
            newRoom.save()
            return HttpResponseRedirect(reverse('juakstore:roomDetail', args=(newRoom.id,)))
        else:
            return render(request, 'juakstore/room_add.html', {'form' : f})
    else:
        return HttpResponseRedirect(reverse('juakstore:roomCreate'))

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

class RoomView(generic.DetailView):
    model = Room
    template_name = 'juakstore/room_detail.html'
    year = None
    month = None

    def get_context_data(self, **kwargs):
        context = super(RoomView, self).get_context_data(**kwargs)
        context['room_bookings'] = Booking.objects.all().filter(room_id=kwargs['object'].id)
        try:
            context['year'] = int(context['year'])
        except KeyError:
            context['year'] = datetime.datetime.now().year
        try:
            context['month'] = int(context['month'])
        except KeyError:
            context['month'] = datetime.datetime.now().month
        return context

class RoomCreate(generic.edit.CreateView):
    model = Room
    template_name = 'juakstore/room_add.html'
    form_class = RoomForm