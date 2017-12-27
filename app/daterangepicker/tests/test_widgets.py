# File: daterangepicker/tests/test_widgets.py
from django.test import TestCase
from django.utils import timezone
from django.utils.formats import localize_input

from django.forms import ValidationError
from django.forms.utils import to_current_timezone

from daterangepicker.widgets import time_range_validator, DateTimeRangeWidget

import datetime

DATETIME_FORMAT = '%m/%d/%Y %I:%M %p'


class TimeRangeValidatorTestCase(TestCase):

    def setUp(self):
        self.today = timezone.now() + datetime.timedelta(minutes=1)
        
        self.yesterday = self.today - datetime.timedelta(hours=24)
        self.tomorrow = self.today + datetime.timedelta(hours=24)

    def test_bad_time_range_string(self):
        """ Test an improperly formatted time range (string) """
        time_range = "yo momma"
        
        with self.assertRaises(ValidationError):
            time_range_validator(time_range)    

    def test_bad_time_range_shorter(self):
        """ Test an improperly formatted time range (list with 1 date)"""
        time_range = [self.today]
        
        with self.assertRaises(ValidationError):
            time_range_validator(time_range)    

    def test_bad_time_range_longer(self):
        """ Test an improperly formatted time range (list with >2 dates) """
        time_range = [self.today, self.today, self.today, self.today]
        
        with self.assertRaises(ValidationError):
            time_range_validator(time_range)    

    def test_early_start(self):
        """ Test time_range_validator with a start date in the past """
        time_range = [self.yesterday, self.today]
        
        with self.assertRaises(ValidationError):
            time_range_validator(time_range)    
    
    def test_soon_start(self):
        """ Test time_range_validator with a start date in the very near future """
        time_range = [self.today, self.today]
        
        time_range_validator(time_range)    

    def test_late_start(self):
        """ Test time_range_validator with a start date in the future """
        time_range = [self.tomorrow, self.tomorrow]
        
        time_range_validator(time_range)    

    def test_early_end(self):
        """ Test time_range_validator with an end date in the past """
        time_range = [self.yesterday, self.yesterday]
        
        with self.assertRaises(ValidationError):
            time_range_validator(time_range)    

    def test_end_before_start(self):
        """ Test time_range_validator with an end date before the start date """
        time_range = [self.today, self.yesterday]
        
        with self.assertRaises(ValidationError):
            time_range_validator(time_range)    

    def test_end_after_start(self):
        """ Test time_range_validator with an end date after the start date """
        time_range = [self.today, self.tomorrow]
        
        time_range_validator(time_range)    


class DateTimeRangeWidgetTestCase(TestCase):

    def setUp(self):
        self.widget = DateTimeRangeWidget()

        self.now = timezone.now()
        self.tomorrow = self.now + datetime.timedelta(hours=24)

    def test_format_value_given_string(self):
        """ Test format_value given an already-correct string """
        time_range = "{} - {}".format( 
                    localize_input(to_current_timezone(self.now), DATETIME_FORMAT),
                    localize_input(to_current_timezone(self.now), DATETIME_FORMAT)
                )
        
        self.assertEqual(self.widget.format_value(time_range), time_range)

    def test_format_value_time_range_too_many(self):
        """ Test format_value with a time_range containing too many values """
        time_range = [self.now, self.tomorrow, self.tomorrow]

        with self.assertRaises(ValueError):
            self.widget.format_value(time_range)

    def test_format_value_time_range_correct(self):
        """ Test format value with a time_range containing two dates in the near future """
        time_range = [self.now, self.tomorrow]

        expected = "{} - {}".format( 
                    localize_input(to_current_timezone(self.now), DATETIME_FORMAT),
                    localize_input(to_current_timezone(self.tomorrow), DATETIME_FORMAT)
                )

        self.assertEqual(self.widget.format_value(time_range), expected)

    def test_format_value_given_none(self):
        """ Test format_value given None for time_range """
    
        # Note: since the value of timezone.now() will be slightly later when
        # run in format_value as compared to the value in setUp, we cannot
        # compare equivalency directly.  
        #
        # Instead, we will convert the output string into a datetime object,
        # and compare the times against an epsilon value of 1 minute, i.e. the
        # difference in date/times is expected to be no more than 1 minute.
        # This is similar to the process for comparing arbitrary floating-point
        # values.

        result = self.widget.format_value(time_range=None)
        start, end, *extra = result.split(" - ")

        self.assertFalse(extra, 
                "Too many dates in output")
        
        self.assertEqual(start, end, 
                "Start date not equivalent to end date")

        result_datetime = datetime.datetime.strptime(start, DATETIME_FORMAT) 
        expected_datetime = to_current_timezone(self.now).replace(second=0,
                microsecond=0)

        diff = result_datetime - expected_datetime

        self.assertGreaterEqual(result_datetime, expected_datetime,
                "format_value gave current date/time earlier than it actually was")

        self.assertLessEqual(diff, datetime.timedelta(minutes=1), 
                "format_value gave an inaccurate current date/time")



