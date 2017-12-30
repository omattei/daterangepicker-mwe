# File: daterangepicker/tests/test_widgets.py
from django.test import TestCase
from django.utils import timezone

from django.forms import ValidationError
from django.forms.utils import to_current_timezone

from django.utils.formats import localize_input

from daterangepicker.forms import time_range_generator, DATETIME_INPUT_FORMAT
from daterangepicker.fields import DateTimeRangeField

import datetime


class BaseDateTimeRangeFieldTestCase(TestCase):
    
    def setUp(self):
        self.field = DateTimeRangeField()
        
        self.today = timezone.now() + datetime.timedelta(minutes=1)
        
        self.yesterday = self.today - datetime.timedelta(hours=24)
        self.tomorrow = self.today + datetime.timedelta(hours=24)
        
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
            DateTimeRangeField(initial=(self.today, ))
    
    def test_init_initial_too_many(self):
        """ 
        Test initializer with more than 2 initial date/times to ensure that
        ValueError is raised
        
        """
        with self.assertRaises(ValueError):
            DateTimeRangeField(
                    initial=(self.today, self.today, self.today, self.today),
                )

    def test_init_two_values(self):
        """ 
        Test initializer with two initial start and end times to ensure that
        subfields are set up properly
        
        """
        field = DateTimeRangeField(initial=(self.today, self.today))
        
        self.assertEqual(field.fields[0].initial, self.today)
        self.assertEqual(field.fields[1].initial, self.today)

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
        time_range = (self.yesterday, self.today)
        
        self.assertEqual(self.field.compress(time_range), tuple(time_range))

    def test_compress_too_many(self):
        """ Test compress method with more than 2 date/times """ 
        time_range = (self.tomorrow, self.tomorrow, 
                      self.tomorrow, self.tomorrow)
        
        with self.assertRaises(ValidationError):
            self.field.compress(time_range)

    def test_clean_bad_time_range_string(self):
        """ Test an improperly formatted time range (arbitrary string) """
        time_range_str = "yo momma"
        
        with self.assertRaises(ValidationError):
            self.field.clean(time_range_str)
    
    def test_clean_bad_time_range_shorter(self):
        """ Test an improperly formatted time range (single date)"""
        time_range_str = localize_input(
                            to_current_timezone(self.today), 
                            DATETIME_INPUT_FORMAT
                        )
        
        with self.assertRaises(ValidationError):
            self.field.clean(time_range_str)

    def test_clean_bad_time_range_longer(self):
        """ Test an improperly formatted time range (tuple with >2 dates) """
        time_range = [
                        localize_input(
                                to_current_timezone(self.today), 
                                DATETIME_INPUT_FORMAT
                            ), 
                    ] * 4
        time_range_str = " - ".join(time_range)
        
        with self.assertRaises(ValidationError):
            self.field.clean(time_range_str)

    def test_clean_soon_start(self):
        """ 
        Test clean with a start date in the very near future 
       
        """
        time_range_str = time_range_generator(self.today, self.today)
        
        self.field.clean(time_range_str)

    def test_clean_late_start(self):
        """ Test clean with a start date in the future """
        time_range_str = time_range_generator(self.tomorrow, self.tomorrow)
        
        self.field.clean(time_range_str)

    def test_clean_end_before_start(self):
        """
        Test clean with an end date before the start date 
        
        """
        time_range_str = time_range_generator(self.today, self.yesterday)
        
        with self.assertRaises(ValidationError):
            self.field.clean(time_range_str)

    def test_clean_end_after_start(self):
        """
        Test clean with an end date after the start date 
        
        """
        time_range_str = time_range_generator(self.today, self.tomorrow)
        
        self.field.clean(time_range_str)


class DateTimeRangeFieldTestCase(BaseDateTimeRangeFieldTestCase):
    
    def test_clean_early_start(self):
        """ Test clean with a start date in the past """
        time_range_str = time_range_generator(self.yesterday, self.today)
        
        with self.assertRaises(ValidationError):
            self.field.clean(time_range_str)
    
    def test_clean_early_end(self):
        """ Test clean with an end date in the past """
        time_range_str = time_range_generator(self.yesterday, self.yesterday)
        
        with self.assertRaises(ValidationError):
            self.field.clean(time_range_str)


class DateTimeRangeFieldAllowsPastTestCase(BaseDateTimeRangeFieldTestCase):
    
    def setUp(self):
        super(DateTimeRangeFieldAllowsPastTestCase, self).setUp()
        self.field.allow_past = True

    def test_clean_early_start(self):
        """ Test clean with a start date in the past """
        time_range_str = time_range_generator(self.yesterday, self.today)
        
        self.field.clean(time_range_str)

    def test_clean_early_end(self):
        """ Test clean with an end date in the past """
        time_range_str = time_range_generator(self.yesterday, self.yesterday)
        
        self.field.clean(time_range_str)

