# File: daterangepicker/widgets.py
from django.forms import ValidationError, TextInput
from django.forms.fields import DateTimeField, MultiValueField
from django.forms.utils import to_current_timezone, from_current_timezone

from django.utils import formats, timezone
from django.utils.translation import gettext_lazy as _

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


class DateTimeRangeWidget(TextInput):
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


class DateTimeRangeField(MultiValueField):
    widget = DateTimeRangeWidget
    default_validators = [time_range_validator, ]

    def __init__(self, initial=None, **kwargs):
        if initial is None:
            initial = [None, None]
        elif len(initial) != 2:
            raise ValueError(_("Initial data list was expected to have exactly"
                + " two dates."))

        fields = (
                    DateTimeField(
                            initial=initial[0],
                            input_formats=[DATETIME_FORMAT, ],
                            **kwargs,
                        ),
                    DateTimeField(
                            initial=initial[1],
                            input_formats=[DATETIME_FORMAT, ],
                            **kwargs,
                        ),
                )

        super(DateTimeRangeField, self).__init__(fields, **kwargs)

    def clean(self, value):
        _time_range = value.strip().split(' - ')

        return super(DateTimeRangeField, self).clean(_time_range)

    def compress(self, data_list):
        try:
            start_time, end_time, *extra = data_list
        except (KeyError, ValueError):
            raise ValidationError(_("Expected two valid dates."))

        if extra: 
            raise ValidationError(_("Expected exactly two dates."))

        return start_time, end_time

