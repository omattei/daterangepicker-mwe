# File: daterangepicker/tests/test_widgets.py
from django.test import TestCase
from django.utils import timezone

from django.forms.utils import to_current_timezone

from daterangepicker.forms import time_range_generator, DATETIME_INPUT_FORMAT
from daterangepicker.widgets import DateTimeRangeWidget

import datetime


class DateTimeRangeWidgetTestCase(TestCase):

    def setUp(self):
        self.widget = DateTimeRangeWidget()

        self.now = timezone.now()
        self.tomorrow = self.now + datetime.timedelta(hours=24)

    def test_format_value_given_string(self):
        """ Test format_value given an already-correct string """
        time_range = time_range_generator(self.now, self.now)
        
        self.assertEqual(self.widget.format_value(time_range), time_range)

    def test_format_value_time_range_too_many(self):
        """ Test format_value with a time_range containing too many values """
        time_range = (self.now, self.tomorrow, self.tomorrow)

        with self.assertRaises(ValueError):
            self.widget.format_value(time_range)

    def test_format_value_time_range_correct(self):
        """ 
        Test format value with a time_range containing two dates in the
        near future 
        
        """
        time_range = (self.now, self.tomorrow)
        expected = time_range_generator(self.now, self.tomorrow)

        self.assertEqual(self.widget.format_value(time_range), expected)
    
    def test_format_value_given_none_none(self):
        """ Test format_value given (None, None) for time_range """
        result = self.widget.format_value(
                        time_range=(None, None),
                    )
        
        # Split returned string by separator
        start, end, *extra = result.split(" - ")
        
        # There should be no items in the extra list
        self.assertFalse(extra, "Too many dates in output")
        # Start time and end time both should be the same by default
        self.assertEqual(start, end, "Start date not equivalent to end date")

        # Current hour is found by getting the current time in the current
        # timezone and rounding down to the closest hour (i.e. replacing
        # the minutes, seconds, and microseconds in the datetime object
        # with 0).
        cur_hour = to_current_timezone(self.now).replace(
                        minute=0,
                        second=0,
                        microsecond=0,
                    ) 
        # Round current time up to nearest hour.
        expected = cur_hour + datetime.timedelta(hours=1)
    
        # Parse actual start time into datetime object
        actual = datetime.datetime.strptime(start,
                DATETIME_INPUT_FORMAT) 
        
        # (Case I) The actual time and expected time should almost always be
        # equal, since they are the result of rounding up to the closest hour. 
        #
        # (Case II) The only exception to this rule is when the "expected" time
        # (time at the start of the test) is right on the edge of the next
        # hour, meaning the "actual" time assigned to both ends of the
        # time_range field could run over into the next hour.
        #
        # Examples:
        #
        # Case I) 
        #
        #    value       yyyy-mm-dd hh-mm-ss.µµµµµµ
        # -----------   ----------------------------
        #   expected  =  2017-12-29 02:26:59.896882
        #             =  2017-12-29 03:00:00.000000
        #    actual   =  2017-12-29 02:27:59.341242
        #             =  2017-12-29 03:00:00.000000
        # Case II) 
        #
        #    value       yyyy-mm-dd hh-mm-ss.µµµµµµ
        # -----------   ----------------------------
        #   expected  =  2017-12-29 02:59:59.896882
        #             =  2017-12-29 03:00:00.000000
        #    actual   =  2017-12-29 03:00:01.341242
        #             =  2017-12-29 04:00:00.000000
        #
        self.assertLessEqual(actual - expected, datetime.timedelta(hours=1), 
                "format_value gave a current date/time outside the expected "
                + "1-hour error threshhold")

    def test_format_value_given_none(self):
        """ Test format_value given None for time_range """
        result = self.widget.format_value(time_range=None)
        
        # Split returned string by separator
        start, end, *extra = result.split(" - ")
        
        # There should be no items in the extra list
        self.assertFalse(extra, "Too many dates in output")
        # Start time and end time both should be the same by default
        self.assertEqual(start, end, "Start date not equivalent to end date")

        # Current hour is found by getting the current time in the current
        # timezone and rounding down to the closest hour (i.e. replacing
        # the minutes, seconds, and microseconds in the datetime object
        # with 0).
        cur_hour = to_current_timezone(self.now).replace(
                        minute=0,
                        second=0,
                        microsecond=0,
                    ) 
        # Round current time up to nearest hour.
        expected = cur_hour + datetime.timedelta(hours=1)
    
        # Parse actual start time into datetime object
        actual = datetime.datetime.strptime(start,
                DATETIME_INPUT_FORMAT) 
        
        # (Case I) The actual time and expected time should almost always be
        # equal, since they are the result of rounding up to the closest hour. 
        #
        # (Case II) The only exception to this rule is when the "expected" time
        # (time at the start of the test) is right on the edge of the next
        # hour, meaning the "actual" time assigned to both ends of the
        # time_range field could run over into the next hour.
        #
        # Examples:
        #
        # Case I) 
        #
        #    value       yyyy-mm-dd hh-mm-ss.µµµµµµ
        # -----------   ----------------------------
        #   expected  =  2017-12-29 02:26:59.896882
        #             =  2017-12-29 03:00:00.000000
        #    actual   =  2017-12-29 02:27:59.341242
        #             =  2017-12-29 03:00:00.000000
        # Case II) 
        #
        #    value       yyyy-mm-dd hh-mm-ss.µµµµµµ
        # -----------   ----------------------------
        #   expected  =  2017-12-29 02:59:59.896882
        #             =  2017-12-29 03:00:00.000000
        #    actual   =  2017-12-29 03:00:01.341242
        #             =  2017-12-29 04:00:00.000000
        #
        self.assertLessEqual(actual - expected, datetime.timedelta(hours=1), 
                "format_value gave a current date/time outside the expected "
                + "1-hour error threshhold")


