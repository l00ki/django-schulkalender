from django import forms
from .models import Event


class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = ["title", "location", "recipients", "start_date", "start_period", "start_time",
                  "end_date", "end_period", "end_time", "all_day", "description"]


class FilterForm(forms.Form):
    query = forms.CharField(max_length=100, required=False)


