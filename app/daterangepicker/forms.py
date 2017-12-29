# File: daterangepicker/forms.py
from django.forms import ModelForm
from django.conf import settings

from django.utils.dateformat import format
from django.utils.formats import localize_input

from django.forms.utils import to_current_timezone

from daterangepicker import utils
from daterangepicker.utils import DATETIME_INPUT_FORMAT, time_range_str

from daterangepicker.widgets import DateTimeRangeField


class TimeRangedModelForm(ModelForm):
    time_range = DateTimeRangeField()

    class Meta:
        # Since time_range isn't actually a field in the model, exclude it from
        # being saved into the new model instance.
        exclude = ['time_range', ]

    def __init__(self, *args, **kwargs):
        super(TimeRangedModelForm, self).__init__(*args, **kwargs)
       
        # Get rid of time_start and time_end fields, which should still have been
        # in the subclass's Meta.fields list.
        self.fields.pop('time_start', None)
        self.fields.pop('time_end', None)
        
        time_start = self.initial.pop('time_start', None)
        time_end = self.initial.pop('time_end', None)
        
        # Set a default time_range if it was not already provided.
        self.initial.setdefault('time_range', (time_start, time_end))

    def save(self, commit=True):
        """ 
        Extend saving such that time_start and time_end values are manually
        set in the model instance. 
        
        """
        super(TimeRangedModelForm, self).save(commit=False)

        time_start, time_end = self.cleaned_data['time_range']

        self.instance.time_start = time_start
        self.instance.time_end = time_end
        
        if commit:
            self.instance.save()

        return self.instance

