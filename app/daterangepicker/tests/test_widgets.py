# File: daterangepicker/tests/test_widgets.py
from django.test import TestCase
from django.utils import timezone
from django.forms import ValidationError

from daterangepicker.widgets import time_range_validator
from daterangepicker import widgets

import datetime


class TimeRangeValidatorTestCase(TestCase):

    def setUp(self):
        self.today = timezone.now() + datetime.timedelta(minutes=1)
        
        self.yesterday = self.today - datetime.timedelta(hours=24)
        self.tomorrow = self.today + datetime.timedelta(hours=24)

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

