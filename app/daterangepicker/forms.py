# File: daterangepicker/forms.py
from django.forms import ModelForm
from django.conf import settings

from django.utils.dateformat import format
from django.utils.formats import localize_input

from django.forms.utils import to_current_timezone

from daterangepicker.widgets import DateTimeRangeField

DATETIME_INPUT_FORMAT = '%m/%d/%Y %I:%M %p'


def time_range_str(start, end, html=False):
    """ 
    Generate time range strings from a given start and end date/time. 
    
    If html is True, a string of the format

        "Dec. 28, 2017, 3:30 a.m. &ndash; Dec. 28, 2017, 3:30 a.m."

    will be returned. Otherwise, we will return a string of the format

        "12/28/2017 03:30 AM - 12/28/2017 03:30 AM"

    """

    # The seperator to use between start and end date/times
    separator = ' &ndash; ' if html else ' - '

    # The function to use to format a datetime object into a string
    datetime_fmtr_func = format if html else localize_input

    # The string format to be used by the date/time formatter function
    fmt_str = settings.DATETIME_FORMAT if html else DATETIME_INPUT_FORMAT

    return '{}{}{}'.format(
                datetime_fmtr_func(to_current_timezone(start), fmt_str),
                separator,
                datetime_fmtr_func(to_current_timezone(end), fmt_str),
            )


class TimeRangedModelForm(ModelForm):
    class Meta:
        # Since time_range isn't actually a field in the model, exclude it from
        # being saved into the new model instance.
        exclude = ['time_range', ]

    def __init__(self, *args, **kwargs):
        super(TimeRangedModelForm, self).__init__(*args, **kwargs)
       
        # Get rid of time_start and time_end fields, if they were accidentally
        # included still.
        self.fields.pop('time_start', None)
        self.fields.pop('time_end', None)
        
        # If we are updating an existing object, make sure the time_range
        # defaults reflect this.
        if 'instance' in kwargs:
            self.fields['time_range'] = DateTimeRangeField(
                            initial=[
                                self.instance.time_start, 
                                self.instance.time_end
                            ]
                        )
        else:
            self.fields['time_range'] = DateTimeRangeField()

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

