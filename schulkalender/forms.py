from django import forms
from .models import Event

import datetime


class DatePickerInput(forms.DateInput):
    input_type = 'date'


class TimePickerInput(forms.TimeInput):
    input_type = 'time'


class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = ["title", "recipients", "start_date", "start_period", "start_time",
                  "end_date", "end_period", "end_time", "location", "all_day", "teacher_only", "description"]
        widgets = {"start_date": DatePickerInput(),
                   "start_time": TimePickerInput(),
                   "end_date": DatePickerInput(),
                   "end_time": TimePickerInput()}


class FilterForm(forms.Form):
    query = forms.CharField(max_length=100, required=False)


