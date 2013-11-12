__author__ = 'wyeung'
from django import forms
from django.forms.extras.widgets import SelectDateWidget
from django.core.exceptions import ValidationError
from widgets import SelectTimeWidget
import datetime
from django.db.models import Q
from juakstore.models import Booking, Room

class BookingForm(forms.ModelForm):
    date = forms.DateField(widget=SelectDateWidget)
    start = forms.TimeField(widget=SelectTimeWidget(twelve_hr=True, minute_step=10))
    end = forms.TimeField(widget=SelectTimeWidget(twelve_hr=True, minute_step=10))

    class Meta:
        model = Booking

    def clean(self):
        cleaned_data = super(BookingForm, self).clean()
        print cleaned_data
        if (cleaned_data.get('start') >= cleaned_data.get('end')):
            raise ValidationError('Event end must be after the start', code='endbeforestart')
        # now check if there are any bookings that overlap with the submitted one
        overlap = Booking.objects.all().filter(room_id=cleaned_data.get('room')).filter(date=cleaned_data.get('date')).filter(
                                    (Q(start__gte=cleaned_data.get('start')) &
                                      Q(start__lte=cleaned_data.get('end')))
                                      | (Q(end__gte=cleaned_data.get('start')) &
                                              Q(end__lte=cleaned_data.get('end'))))
        if self.id:
            overlap = overlap.filter(~Q(id=self.id))
        print cleaned_data
        print overlap
        if overlap.count() > 0:
            raise ValidationError('Conflicts with another booking', code='conflictingbooking')
        return cleaned_data

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room