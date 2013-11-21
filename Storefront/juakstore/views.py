from django.views import generic
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, render_to_response
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext, loader
from django.contrib.auth.models import User
from models import Booking, BookingCategory, Room, Partner
from forms import BookingForm, RoomForm, BookingEditForm, PartnerForm
from mycalendar import BookingCalendar
from django.utils.safestring import mark_safe
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from django.core.mail import send_mail

import datetime

from django.forms.models import model_to_dict

@login_required
def index(request):
    if request.method == "GET":
        if 'year' in request.GET:
            year = int(request.GET['year'])
        else:
            year = datetime.datetime.now().year
        if 'month' in request.GET:
            month = int(request.GET['month'])
        else:
            month = datetime.datetime.now().month
        if 'day' in request.GET:
            day = int(request.GET['day'])
        else:
            day = datetime.datetime.now().day

    template = loader.get_template('juakstore/index.html')
    newBooking = BookingForm()
    all_bookings = Booking.objects.all()
    all_rooms = Room.objects.all()
    if request.user.is_authenticated():
        currentUser = request.user    
    context = RequestContext(request, {
        'all_bookings': all_bookings,
        'all_rooms': all_rooms,
        'year': year,
        'currentUser' : currentUser,
        'month': month,
        'day': day,
        'form': newBooking
    })
    return HttpResponse(template.render(context))

@staff_member_required
def adminView(request):
    template = loader.get_template('juakstore/admin_view.html')
    partners = Partner.objects.all()
    users = User.objects.all()
    bookings = Booking.objects.all()
    noUsers = False
    noBookings = False
    count = 0
    bcount = 0
    for u in users:
        if u.is_active == False:
            count = count + 1
    if count == 0:
        noUsers = True
    for b in bookings:
        if b.approved == False:
            bcount = bcount + 1
    if bcount == 0:
        noBookings = True        
    if request.user.is_authenticated():
        currentUser = request.user    
    context = RequestContext(request, {
        'partners': partners,
        'currentUser': currentUser,
        'bookings': bookings,
        'noUsers': noUsers,
        'noBookings': noBookings
    }) 
    return HttpResponse(template.render(context)) 

@staff_member_required
def accept(request, pk):
    if request.method == "POST":
        b = get_object_or_404(User, pk=pk)
        f = PartnerForm(request.POST)
        f.id = pk
        
        b.is_active = True
        b.save()
        #send email notification
        subject = "East Scarborough Storefront - Account Approved"
        message = "Dear " + b.username + ",\n\nYour account request at East Scarborough Storefront has been approved.\nYou can login at <URL>.\n\nThank you"
        b.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)
        return render(request, 'juakstore/admin_accept.html', {'user': b})
    else:
        form = BookingForm()
        return HttpResponseRedirect(reverse('juakstore/admin_accept.html', args=(pk,)))
    
@staff_member_required
def acceptBooking(request, pk):
    if request.method == "POST":
        b = get_object_or_404(Booking, pk=pk)
        f = BookingForm(request.POST)
        f.id = pk
        
        b.approved = True
        b.save()
        #send email notification
        subject = "East Scarborough Storefront - Booking Approved"
        message = "Dear " + b.booker.username + ",\n\nYour booking request '" + b.name + "' at East Scarborough Storefront has been approved.\nYou can login at <URL>.\n\nThank you"
        b.booker.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)
        return render(request, 'juakstore/admin_acceptBooking.html', {'booking': b})
    else:
        form = BookingForm()
        return HttpResponseRedirect(reverse('juakstore/admin_acceptBooking.html', args=(pk,)))
   

@login_required
def addBooking(request):
    if request.method == "POST":
        f = BookingForm(request.POST, initial={'booker':request.user, 'room':0})
        if f.is_valid():
            first_booking = 0
            for room in f.cleaned_data['room']:
                newBooking = Booking(name=f.cleaned_data['name'],
                              notes=f.cleaned_data['notes'],
                              date=f.cleaned_data['date'],
                              start=f.cleaned_data['start'],
                              end=f.cleaned_data['end'],
                              booker=get_object_or_404(User, pk=request.user.id),
                              category=get_object_or_404(BookingCategory, pk=request.POST['category']),
                              room=get_object_or_404(Room, pk=room.pk))
                newBooking.save()
                if first_booking == 0:
                    first_booking = newBooking.id

                if (f.cleaned_data['repeat']): # repeat is specified
                    curr_date = f.cleaned_data['date']

                    ''' Timestep will be the increment for the repeat '''
                    if f.cleaned_data['repeat_frequency_unit'] == 'day':
                        timestep =  datetime.timedelta(days=f.cleaned_data['repeat_frequency'])
                    elif f.cleaned_data['repeat_frequency_unit'] == 'week':
                        timestep = datetime.timedelta(weeks=f.cleaned_data['repeat_frequency'])
                    elif f.cleaned_data['repeat_frequency_unit'] == 'month':
                        timestep = datetime.timedelta(weeks=4 * f.cleaned_data['repeat_frequency'])

                    while curr_date + timestep <= f.cleaned_data['repeat_end'] and timestep:
                        curr_date += timestep
                        repeatBooking = Booking(name=f.cleaned_data['name'],
                              notes=f.cleaned_data['notes'],
                              date=curr_date,
                              start=f.cleaned_data['start'],
                              end=f.cleaned_data['end'],
                              booker=get_object_or_404(User, pk=request.user.id),
                              category=get_object_or_404(BookingCategory, pk=request.POST['category']),
                              room=get_object_or_404(Room, pk=room.pk))
                        repeatBooking.save()
            # notify all admins of booking request
            admins = User.objects.filter(is_staff=True) 
            subject = "East Scarborough Storefront - Booking Request"
            message = request.user.username + " has requested a booking.\n\nBooking info:\n <INFO>"
            for a in admins:
                a.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)                        
            return HttpResponseRedirect(reverse('juakstore:bookingDetail',
                                                args=(first_booking,)))
        else:
            return render(request, 'juakstore/booking_add.html', {'form': f,
                                                                  'all_bookings':Booking.objects.all(),
                                                                  'year': datetime.datetime.now().year,
                                                                  'month': datetime.datetime.now().month,
                                                                  })
    else:
        return HttpResponseRedirect(reverse('juakstore:bookingCreate'))

@login_required
def calendar(request, year, month):
    foundBookings = Booking.objects.order_by(date__year=year, date__month=month)
    cal  = BookingCalendar(foundBookings).formatmonth(year, month)
    return render_to_response('index.html', {'calendar':mark_safe(cal),})

@login_required
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
            for room in f.cleaned_data['room']:
                b.name = f.cleaned_data['name']
                b.notes = f.cleaned_data['notes']
                b.start = f.cleaned_data['start']
                b.end = f.cleaned_data['end']
                b.category = get_object_or_404(BookingCategory, pk=request.POST['category'])
                b.room = get_object_or_404(Room, pk=room.pk)
                b.save()
            return HttpResponseRedirect(reverse('juakstore:bookingDetail', args=(b.id,)))
        else:
            return render(request, 'juakstore/booking_update.html', {'form': f, 'booking': b})
    else:
        form = BookingForm()
        return HttpResponseRedirect(reverse('juakstore:bookingDetail', args=(pk,)))

@login_required
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

@login_required
def displayBooking(request, pk):
    b = get_object_or_404(Booking, pk=pk)
    if request.user.is_authenticated():
        c = request.user       
    return render(request, 'juakstore/bookingdetail.html', {'booking':b, 'currentUser':c})

@login_required
def logoutStorefront(request):
    logout(request)
    return HttpResponseRedirect(reverse('juakstore:index'))

class BookingView(generic.DetailView):
    model = Booking
    template_name = 'juakstore/bookingdetail.html'

class BookingCreate(generic.edit.CreateView):
    model = Booking
    template_name = 'juakstore/booking_add.html'
    form_class = BookingForm
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month

    def get(self, request):
        if 'year' in request.GET:
            self.year = int(request.GET['year'])
        #else:
        #    year = datetime.datetime.now().year
        if 'month' in request.GET:
            self.month = int(request.GET['month'])
        #else:
        #    month = datetime.datetime.now().month
        all_bookings = Booking.objects.all()
        form = self.form_class(initial=self.initial)
        template = loader.get_template(self.template_name)
        context = RequestContext(request, {
            'year': self.year,
            'month': self.month,
            'form': form,
            'all_bookings': all_bookings,
        })
        return HttpResponse(template.render(context))

    def get_context_data(self, **kwargs):
        context = super(BookingCreate, self).get_context_data(**kwargs)
        context['allbookings'] = Booking.objects.all()
        context['year'] = datetime.datetime.now().year
        context['month'] = datetime.datetime.now().month
        return context

class BookingUpdate(generic.edit.UpdateView):
    model = Booking
    template_name = 'juakstore/booking_update.html'
    form_class = BookingEditForm

class UserDetailView(generic.DetailView):
    model = User
    template_name = 'juakstore/user.html'

class RoomList(generic.ListView):
    model = Room
    template_name = "juakstore/room_list.html"

class RoomView(generic.DetailView):
    model = Room
    template_name = 'juakstore/room_detail.html'

    def get(self, request, *args, **kwargs):
        if 'year' in request.GET:
            year = int(request.GET['year'])
        else:
            year = datetime.datetime.now().year
        if 'month' in request.GET:
            month = int(request.GET['month'])
        else:
            month = datetime.datetime.now().month
        room_bookings = Booking.objects.all().filter(room_id=kwargs['pk'])
        context = RequestContext(request, {
            'year': year,
            'month': month,
            'room_bookings': room_bookings,
            'room': Room.objects.all().filter(id=kwargs['pk'])[0]
        })
        template = loader.get_template(self.template_name)
        return HttpResponse(template.render(context))

    def get_context_data(self, **kwargs):
        context = super(RoomView, self).get_context_data(**kwargs)
        context['room_bookings'] = Booking.objects.all().filter(room_id=kwargs['object'].id)
        try:
            context['year'] = self.year
        except KeyError:
            context['year'] = datetime.datetime.now().year
        try:
            context['month'] = self.month
        except KeyError:
            context['month'] = datetime.datetime.now().month
        return context

class RoomCreate(generic.edit.CreateView):
    model = Room
    template_name = 'juakstore/room_add.html'
    form_class = RoomForm
