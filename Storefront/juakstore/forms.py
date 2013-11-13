__author__ = 'wyeung'
from django import forms
from django.forms.extras.widgets import SelectDateWidget
from django.core.exceptions import ValidationError
from widgets import SelectTimeWidget
import datetime
from django.db.models import Q
from juakstore.models import Booking, Room

class BookingForm(forms.ModelForm):
    repeat_choices = [
        ('day', 'day(s)'),
        ('week', 'week(s)'),
        ('month', 'month(s)')
    ]

    date = forms.DateField(widget=SelectDateWidget)
    start = forms.TimeField(widget=SelectTimeWidget(twelve_hr=True, minute_step=10))
    end = forms.TimeField(widget=SelectTimeWidget(twelve_hr=True, minute_step=10))

    #repeat = forms.BooleanField(widget=forms.CheckboxInput(attrs={'onChange': 'showHideFrequency(this.value)'}))
    repeat = forms.BooleanField(required=False)

    repeat_frequency = forms.IntegerField(required=False)
    repeat_frequency_unit = forms.ChoiceField(choices=repeat_choices, required=False)
    repeat_end = forms.DateField(widget=SelectDateWidget, required=False)

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
        try:
            if self.id:
                # filter for the ones that are not itself, in the case of
                # an edit, the booking will conflict with itself
                overlap = overlap.filter(~Q(id=self.id))
        except:
            # must be a new booking since there is no id
            pass

        if (cleaned_data.get('repeat')): # repeat is requested
            if not cleaned_data.get('repeat_frequency'): #repeat is requested, but not filled out
                raise ValidationError('Repeat requested but not specified', code='norepeatfrequency')
            if not cleaned_data.get('repeat_end'): #repeat requested, no end date specified
                raise ValidationError('No repeat end date specified', code='norepeatend')
            if cleaned_data.get('repeat_end') < cleaned_data.get('date'): # check if the repeat end date is after the start date
                raise ValidationError('Repeat end date is not after the start date')

        if overlap.count() > 0:
            raise ValidationError('Conflicts with another booking', code='conflictingbooking')
        return cleaned_data

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room