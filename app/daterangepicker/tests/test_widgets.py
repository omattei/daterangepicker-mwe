# File: daterangepicker/tests/test_widgets.py
from django.test import TestCase
from django.utils import timezone

from django.forms import ValidationError
from django.forms.utils import to_current_timezone

from daterangepicker.forms import time_range_str, DATETIME_INPUT_FORMAT
from daterangepicker.widgets import time_range_validator, \
        DateTimeRangeWidget, DateTimeRangeField

import datetime


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
        """ Test an improperly formatted time range (tuple with 1 date)"""
        time_range = (self.today, )
        
        with self.assertRaises(ValidationError):
            time_range_validator(time_range)    

    def test_bad_time_range_longer(self):
        """ Test an improperly formatted time range (tuple with >2 dates) """
        time_range = (self.today, self.today, self.today, self.today)
        
        with self.assertRaises(ValidationError):
            time_range_validator(time_range)    

    def test_early_start(self):
        """ Test time_range_validator with a start date in the past """
        time_range = (self.yesterday, self.today)
        
        with self.assertRaises(ValidationError):
            time_range_validator(time_range)    
    
    def test_soon_start(self):
        """ 
        Test time_range_validator with a start date in the very near future 
       
        """
        time_range = (self.today, self.today)
        
        time_range_validator(time_range)    

    def test_late_start(self):
        """ Test time_range_validator with a start date in the future """
        time_range = (self.tomorrow, self.tomorrow)
        
        time_range_validator(time_range)    

    def test_early_end(self):
        """ Test time_range_validator with an end date in the past """
        time_range = (self.yesterday, self.yesterday)
        
        with self.assertRaises(ValidationError):
            time_range_validator(time_range)    

    def test_end_before_start(self):
        """
        Test time_range_validator with an end date before the start date 
        
        """
        time_range = (self.today, self.yesterday)
        
        with self.assertRaises(ValidationError):
            time_range_validator(time_range)    

    def test_end_after_start(self):
        """
        Test time_range_validator with an end date after the start date 
        
        """
        time_range = (self.today, self.tomorrow)
        
        time_range_validator(time_range)    


class DateTimeRangeWidgetTestCase(TestCase):

    def setUp(self):
        self.widget = DateTimeRangeWidget()

        self.now = timezone.now()
        self.tomorrow = self.now + datetime.timedelta(hours=24)

    def test_format_value_given_string(self):
        """ Test format_value given an already-correct string """
        time_range = time_range_str(self.now, self.now)
        
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
        expected = time_range_str(self.now, self.tomorrow)

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


class DateTimeRangeFieldTestCase(TestCase):
    
    def setUp(self):
        self.field = DateTimeRangeField()
        self.now = timezone.now()
        
        self.yesterday = self.now - datetime.timedelta(hours=24)
        self.tomorrow = self.now + datetime.timedelta(hours=24)

    def test_init_initial_none(self):
        """ 
        Test initializer with no initial start or end times to ensure that
        subfields are set up properly
        
        """
        self.assertIsNone(self.field.fields[0].initial)
        self.assertIsNone(self.field.fields[1].initial)
        
    def test_init_initial_one_only(self):
        """ 
        Test initializer with only one initial date/time to ensure that
        ValueError is raised
        
        """
        with self.assertRaises(ValueError):
            DateTimeRangeField(initial=(self.now, ))
    
    def test_init_initial_too_many(self):
        """ 
        Test initializer with more than 2 initial date/times to ensure that
        ValueError is raised
        
        """
        with self.assertRaises(ValueError):
            DateTimeRangeField(
                        initial=(self.now, self.now, self.now, self.now),
                    )

    def test_init_two_values(self):
        """ 
        Test initializer with two initial start and end times to ensure that
        subfields are set up properly
        
        """
        field = DateTimeRangeField(initial=(self.now, self.now))
        
        self.assertEqual(field.fields[0].initial, self.now)
        self.assertEqual(field.fields[1].initial, self.now)

    def test_clean_valid_string(self):
        """ Test clean method with a valid time_range string """
        time_range = time_range_str(self.now, self.now)

        self.field.clean(time_range)

    def test_clean_invalid_string(self):
        """ Test clean method with an invalid time_range string """
        time_range = "yo momma"

        with self.assertRaises(ValidationError):
            self.field.clean(time_range)

    def test_clean_invalid_range(self):
        """ 
        Test clean method with an illogical time_range that is still a
        "valid" string to ensure it raises an error.
        
        This will test that the default_validators are being run, and thus our
        pre-tested time_range_validator.
        
        """
        time_range = time_range_str(self.yesterday, self.now)

        with self.assertRaises(ValidationError):
            self.field.clean(time_range)

    def test_compress_one_only(self):
        """ Test compress method with only one date/time """ 
        time_range = (self.tomorrow, )
        
        with self.assertRaises(ValidationError):
            self.field.compress(time_range)

    def test_compress_two_correct(self):
        """ Test compress method with two correct date/times """
        time_range = (self.tomorrow, self.tomorrow)
        
        self.assertEqual(self.field.compress(time_range), tuple(time_range))

    def test_compress_two_incorrect(self):
        """
        Test compress method with two incorrect date/times.
        
        Result should be virtually the same as if both date/times were correct,
        as compress does not perform any validation. 
        
        """
        time_range = (self.yesterday, self.now)
        
        self.assertEqual(self.field.compress(time_range), tuple(time_range))

    def test_compress_too_many(self):
        """ Test compress method with more than 2 date/times """ 
        time_range = (self.tomorrow, self.tomorrow, 
                      self.tomorrow, self.tomorrow)
        
        with self.assertRaises(ValidationError):
            self.field.compress(time_range)


