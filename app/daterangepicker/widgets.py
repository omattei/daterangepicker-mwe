# File: daterangepicker/widgets.py
from django.forms import TextInput
from django.forms.utils import to_current_timezone

from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from daterangepicker.utils import time_range_generator

import datetime


class DateTimeRangeWidget(TextInput):
    template_name = "daterangepicker/forms/widgets/datetimerange.html"
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
                minute=0, second=0, microsecond=0,
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
            start_time, end_time, *extra = [to_current_timezone(t) for t in time_range]

            if extra:
                raise ValueError(_("Expected exactly two dates."))

        return time_range_generator(start_time, end_time)

    class Media:
        css = {
            "all": ("daterangepicker/css/styles.css",),
        }
        js = (
            "//cdn.jsdelivr.net/momentjs/latest/moment.min.js",
            "//cdn.jsdelivr.net/bootstrap.daterangepicker/2/" + "daterangepicker.js",
            "daterangepicker/js/script.js",
        )
