# File: daterangepicker/widgets.py
from django import forms 
from django.forms import ValidationError, fields

from django.utils import formats, timezone
from django.utils.translation import gettext_lazy as _
from django.forms.utils import to_current_timezone, from_current_timezone

import datetime

DATETIME_FORMAT = '%m/%d/%Y %I:%M %p'


def time_range_validator(time_range):
    """ Validate that a range of two date/timees makes logical sense. """
    start_time, end_time, *extra = time_range
    
    if extra: 
        raise ValidationError(_("Expected exactly two dates."))

    now = timezone.now().replace(microsecond=0, second=0)

    if start_time < now:
        raise ValidationError(_("Start date is in the past."))

    if end_time < now:
        raise ValidationError(_("End date is in the past."))

    if end_time < start_time:
        raise ValidationError(_("End date is before start date."))


class DateTimeRangeWidget(forms.TextInput):
    template_name = 'daterangepicker/forms/widgets/datetimerange.html'
    supports_microseconds = True

    def __init__(self, attrs=None, format=DATETIME_FORMAT):
        super(DateTimeRangeWidget, self).__init__(attrs)
        self.format = format 
        
    def format_value(self, time_range):
        format = self.format
        
        if isinstance(time_range, str):
            return time_range

        if not time_range:
            now = to_current_timezone(timezone.now())
            start_time, end_time = [now, now]
        else:
            start_time, end_time, *extra = [
                        to_current_timezone(t) for t in time_range
                    ]
    
            if extra: 
                raise ValueError(_("Expected exactly two dates."))


        return '{} - {}'.format(
                    start_time.strftime(format),
                    end_time.strftime(format),
                )

    class Media:
        css = {
                'all': ('daterangepicker/css/styles.css', ),
            }

        js = (
            '//cdn.jsdelivr.net/momentjs/latest/moment.min.js',
            '//cdn.jsdelivr.net/bootstrap.daterangepicker/2/daterangepicker.js',
            'daterangepicker/js/script.js',
        )


class DateTimeRangeField(fields.BaseTemporalField):
    widget = DateTimeRangeWidget
    default_validators = [time_range_validator, ]

    def __init__(self, initial=None, **kwargs):
        super(DateTimeRangeField, self).__init__(
                    input_formats=[DATETIME_FORMAT,],
                    initial=initial,
                    **kwargs,
                )
   
    def to_python(self, value):
        _time_range = value.strip().split(' - ')

        # For each date/time string in the _time_range list:
        #
        # (1) Run the superclass's to_python method to return a timezone-naïve
        #     object.
        # (2) Then, convert that timezone-naïve object into a timezone-aware
        #     object. 
        # 
        # If the list contained more than two strings, these will be placed in
        # the extra list.
        try:
            start_time, end_time, *extra = [
                        from_current_timezone(
                                super(DateTimeRangeField, self).to_python(t)
                            ) 
                        for t in _time_range
                    ]
        except (KeyError, ValueError):
            raise ValidationError(_("Expected two valid dates."))

        if extra: 
            raise ValidationError(_("Expected exactly two dates."))

        return start_time, end_time

    def strptime(self, value, format):
        return datetime.datetime.strptime(value, format)

