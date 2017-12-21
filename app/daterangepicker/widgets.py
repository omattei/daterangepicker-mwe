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

    now = timezone.now()

    if start_time and end_time:
        if start_time < now:
            raise ValidationError(_("Start date is in the past."))

        if end_time < now:
            raise ValidationError(_("End date is in the past."))

        if end_time < start_time:
            raise ValidationError(_("End date is before start date."))


class DateTimeRangeWidget(forms.TextInput):
    template_name = 'daterangepicker/forms/widgets/datetimerange.html'
    supports_microseconds = True

    def __init__(self, attrs=None, format=DATETIME_FORMAT, **kwargs):
        super(DateTimeRangeWidget, self).__init__(attrs)
        self.format = format 

    def format_value(self, value):
        now = timezone.now()
        fmt = self.format

        if not value:
            return '{0} - {0}'.format(formats.localize_input(now, fmt))

        return '{} - {}'.format(
                    formats.localize_input(value[0], fmt),
                    formats.localize_input(value[1], fmt),
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

    def __init__(self, **kwargs):
        super(DateTimeRangeField, self).__init__(
                    input_formats=[DATETIME_FORMAT,],
                    **kwargs,
                )
   
    def to_python(self, value):
        _time_range = value.strip().split(' - ')
        start_time, end_time, *extra = [
                    super(DateTimeRangeField, self).to_python(t.strip()) 
                    for t in _time_range
                ]

        if extra: 
            raise ValidationError(_("Expected exactly two dates."))

        return start_time, end_time

    def strptime(self, value, format):
        return datetime.datetime.strptime(value, format)
