# File: simpleapp/forms.py
from simpleapp.models import Event

from daterangepicker import forms


class EventForm(TimeRangedModelForm):
    model = Event
    fields = '__all__'
