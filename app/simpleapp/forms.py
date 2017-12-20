# File: simpleapp/forms.py
from simpleapp.models import Event

from daterangepicker.forms import TimeRangedModelForm


class EventForm(TimeRangedModelForm):
    model = Event
    fields = '__all__'
