# File: simpleapp/forms.py
from simpleapp.models import Event

from daterangepicker.forms import TimeRangedModelForm
from daterangepicker.fields import DateTimeRangeField


class EventForm(TimeRangedModelForm):
    """ 
    A model form for the Event model that represents the time_start and
    time_end fields in the model with a time_range field in the form.

    """

    class Meta:
        model = Event
        fields = "__all__"


class EventFormAllowsPast(EventForm):
    """ 
    A model form for the Event model that represents the time_start and
    time_end fields in the model with a time_range field in the form. Allows
    time_range to be in the past.

    (It is not currently used in any view function.)

    """

    time_range = DateTimeRangeField(allow_past=True)
