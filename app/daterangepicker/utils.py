# File: daterangepicker/utils.py
from django.conf import settings

from django.utils.dateformat import format
from django.utils.formats import localize_input

from django.forms.utils import to_current_timezone

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

