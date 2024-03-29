__author__ = 'wyeung'
from django import forms
from django.forms.extras.widgets import SelectDateWidget
from django.core.exceptions import ValidationError
from widgets import SelectTimeWidget
import datetime
from django.contrib.auth.models import User
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
    room = forms.ModelMultipleChoiceField(queryset=Room.objects.all())
    booker = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput(), required=False)
    approved = forms.BooleanField(widget=forms.HiddenInput(), required=False) 
    #rooms = forms.ModelChoiceField(widget=forms.HiddenInput(), queryset=Room.objects.all(), required=False)

    #repeat = forms.BooleanField(widget=forms.CheckboxInput(attrs={'onChange': 'showHideFrequency(this.value)'}))
    repeat = forms.BooleanField(required=False)

    repeat_frequency = forms.IntegerField(required=False)
    repeat_frequency_unit = forms.ChoiceField(choices=repeat_choices, required=False)
    repeat_end = forms.DateField(widget=SelectDateWidget, required=False, label="Repeat until")

    def __init__(self, *args, **kwargs):
        super(BookingForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Booking
        exclude = ('booker', 'room',)

    def clean(self):
        error = []
        cleaned_data = super(BookingForm, self).clean()
        if (cleaned_data.get('start') >= cleaned_data.get('end')):
            error.append('Event end must be after the start')
        if (cleaned_data.get('repeat')): # repeat is requested
            if not cleaned_data.get('repeat_frequency'): #repeat is requested, but not filled out
                error.append('Repeat requested but not specified')
                raise ValidationError('Repeat requested but not specified', code='norepeatfrequency')
            if not cleaned_data.get('repeat_end'): #repeat requested, no end date specified
                error.append('No repeat end date specified')
            if cleaned_data.get('repeat_end') < cleaned_data.get('date'): # check if the repeat end date is after the start date
                error.append('Repeat end date is not after the start date')


        if len(error) > 0 :
            raise ValidationError(error)

        return cleaned_data


class BookingEditForm(BookingForm):
    repeat_choices = [
        ('day', 'day(s)'),
        ('week', 'week(s)'),
        ('month', 'month(s)')
    ]

    repeat = forms.BooleanField(required=False, widget=forms.HiddenInput(), initial=False)
    room = forms.ModelChoiceField(queryset=Room.objects.all())
    repeat_frequency = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    repeat_frequency_unit = forms.ChoiceField(widget=forms.HiddenInput(), choices=repeat_choices, required=False)
    repeat_end = forms.DateField(widget=forms.HiddenInput(), required=False)
    updateSeries = forms.BooleanField(required=False,label="Update Series")

    class Meta:
        model = Booking


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        
class PartnerForm(forms.Form):
    activate = forms.BooleanField(label="Activate")     
    partner = forms.ModelChoiceField(queryset=User.objects.all())
    activate = forms.BooleanField(
        error_messages={'required': 'You must accept the terms and conditions'},
        label="Terms&Conditions")    

    def __init__(self, *args, **kwargs):
        super(PartnerForm, self).__init__(*args, **kwargs)

    class Meta:
        model = User
        #exclude = ('booker', 'room',)

    def clean(self):
        error = []
        cleaned_data = super(PartnerForm, self).clean()

        return cleaned_data
