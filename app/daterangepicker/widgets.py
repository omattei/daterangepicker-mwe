# File: daterangepicker/widgets.py
from django.forms import ValidationError, TextInput
from django.forms.fields import DateTimeField, MultiValueField
from django.forms.utils import to_current_timezone

from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from daterangepicker.utils import DATETIME_INPUT_FORMAT, time_range_str

import datetime


def time_range_validator(time_range):
    """ Validate that a range of two date/times makes logical sense. """
    try:
        start_time, end_time, *extra = time_range
    except ValueError:
        raise ValidationError(_("Expected more than one date."))

    if extra: 
        raise ValidationError(_("Expected exactly two dates."))

    now = timezone.now().replace(microsecond=0, second=0)

    if end_time < start_time:
        raise ValidationError(_("End date is before start date."))

    if start_time < now:
        raise ValidationError(_("Start date is in the past."))


class DateTimeRangeWidget(TextInput):
    template_name = 'daterangepicker/forms/widgets/datetimerange.html'
    supports_microseconds = False

    def __init__(self, attrs=None):
        super(DateTimeRangeWidget, self).__init__(attrs)
        
    def format_value(self, time_range):
        if isinstance(time_range, str):
            return time_range

        if not time_range or None in time_range:
            # Current hour is found by getting the current time in the current
            # timezone and rounding down to the closest hour (i.e. replacing
            # the minutes, seconds, and microseconds in the datetime object
            # with 0).
            cur_hour = to_current_timezone(timezone.now()).replace(
                            minute=0,
                            second=0,
                            microsecond=0,
                        ) 
            
            # Default time should be right at the upcoming hour. For example,
            # all of the following current times should be rounded up to
            # 10:00 am:
            # 
            #  - 9:00 am  
            #  - 9:30 am
            #  - 9:59 am
            #  - 9:24 am
            default_time = cur_hour + datetime.timedelta(hours=1)

            start_time = default_time
            end_time = default_time
        else:
            start_time, end_time, *extra = [
                        to_current_timezone(t) for t in time_range
                    ]

            if extra: 
                raise ValueError(_("Expected exactly two dates."))

        return time_range_str(start_time, end_time)

    class Media:
        css = {
                'all': ('daterangepicker/css/styles.css', ),
            }
        js = (
                '//cdn.jsdelivr.net/momentjs/latest/moment.min.js',
                '//cdn.jsdelivr.net/bootstrap.daterangepicker/2/' 
                + 'daterangepicker.js',
                'daterangepicker/js/script.js',
            )


class DateTimeRangeField(MultiValueField):
    widget = DateTimeRangeWidget
    default_validators = [time_range_validator, ]

    def __init__(self, initial=None, **kwargs):
        if initial is None:
            initial = (None, None)
        
        if len(initial) != 2:
            raise ValueError(_("Initial data tuple was expected to have "
                + " exactly two dates."))

        fields = (
                    DateTimeField(
                            initial=initial[0],
                            input_formats=[DATETIME_INPUT_FORMAT, ],
                            **kwargs,
                        ),
                    DateTimeField(
                            initial=initial[1],
                            input_formats=[DATETIME_INPUT_FORMAT, ],
                            **kwargs,
                        ),
                )
       
        super(DateTimeRangeField, self).__init__(
                fields, initial=initial, **kwargs)
    
    def clean(self, time_range):
        _time_range = time_range.split(' - ')

        return super(DateTimeRangeField, self).clean(_time_range)

    def compress(self, data_list):
        try:
            start_time, end_time, *extra = data_list
        except (KeyError, ValueError):
            raise ValidationError(_("Expected two valid dates."))

        if extra: 
            raise ValidationError(_("Expected exactly two dates."))

        return start_time, end_time

