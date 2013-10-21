__author__ = 'wyeung'
from django import forms
from django.forms.extras.widgets import SelectDateWidget
from django.core.exceptions import ValidationError
import datetime

from juakstore.models import Booking

class BookingForm(forms.ModelForm):
    date = forms.DateField(widget=SelectDateWidget)

    class Meta:
        model = Booking

    def clean(self):
        cleaned_data = super(BookingForm, self).clean()
        ve = []
        if(cleaned_data.get('start') >= cleaned_data.get('end')):
            ve.append(ValidationError('Event end must be after the start', code='endbeforestart'))
        if (len(ve) > 0): # there are errors
            raise ValidationError(ve)
        return cleaned_data