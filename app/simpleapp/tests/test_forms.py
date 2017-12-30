# File: simpleapp/tests/test_forms.py
from django.test import TestCase
from django.utils import timezone

from simpleapp.models import Event
from simpleapp.forms import EventForm, EventFormAllowsPast

from daterangepicker.forms import time_range_generator

import datetime


class EventFormTestCase(TestCase):

    def setUp(self):
        self.today = timezone.now() + datetime.timedelta(minutes=1)
        
        self.yesterday = self.today - datetime.timedelta(hours=24)
        self.tomorrow = self.today + datetime.timedelta(hours=24)
        
        self.event = Event.objects.create(
                        title="Test Event",
                        time_start=self.tomorrow,
                        time_end=self.tomorrow,
                    )

    def test_title_still_in_fields(self):
        """
        Test that the title field is still in the form's fields
        
        """
        form = EventForm()

        self.assertIn('title', form.fields)

    def test_fields_replaced(self):
        """
        Test that time_range replaces both time_start and time_end fields in
        the form 
        
        """
        form = EventForm()
        
        self.assertIn('time_range', form.fields)

        self.assertNotIn('time_start', form.fields)
        self.assertNotIn('time_end', form.fields)

    def test_with_existing_instance(self):
        """
        Test to ensure that a pre-existing instance's time_start and time_end
        values are set as defaults for the time_range field

        """
        form = EventForm(instance=self.event)
        
        self.assertEqual(form.initial['time_range'], 
                        (
                            self.event.time_start, 
                            self.event.time_end
                        )
                    )

    def test_save_commit(self):
        """ Test saving a form to database """
        time_range = time_range_generator(self.tomorrow, self.tomorrow)
        data = {
                'title': 'Test Event',
                'time_range': time_range,
            }

        form = EventForm(data)

        self.assertTrue(form.is_valid())

        event = form.save()
        self.assertIsNotNone(event)
        
        self.assertTrue(Event.objects.filter(pk=event.pk).exists())
    
    def test_save_no_commit(self):
        """ Test saving a form without committing directly to database """
        time_range = time_range_generator(self.tomorrow, self.tomorrow)
        data = {
                'title': 'Test Event',
                'time_range': time_range,
            }

        form = EventForm(data)

        self.assertTrue(form.is_valid())

        event = form.save(commit=False)
        self.assertIsNotNone(event)
        self.assertFalse(Event.objects.filter(pk=event.pk).exists())

        event.save() 
        self.assertTrue(Event.objects.filter(pk=event.pk).exists())

    def test_save_bad_time_range(self):
        """
        Ensure that validations are working on the form for bad time range data 
        
        """
        time_range = time_range_generator(self.today, self.yesterday)
        data = {
                'title': 'Test Event',
                'time_range': time_range,
            }

        form = EventForm(data)

        self.assertFalse(form.is_valid())

    def test_denies_past_time_range(self):
        """
        Ensure that a time_range in the past is not considered valid.
        
        """
        time_range = time_range_generator(self.yesterday, self.tomorrow)
        data = {
                'title': 'Test Event',
                'time_range': time_range,
            }

        form = EventForm(data)

        self.assertFalse(form.is_valid())


class EventFormAllowsPastTestCase(TestCase):

    def setUp(self):
        self.today = timezone.now() + datetime.timedelta(minutes=1)
        
        self.yesterday = self.today - datetime.timedelta(hours=24)
        self.tomorrow = self.today + datetime.timedelta(hours=24)
        
        self.event = Event.objects.create(
                        title="Test Event",
                        time_start=self.tomorrow,
                        time_end=self.tomorrow,
                    )

    def test_title_still_in_fields(self):
        """
        Test that the title field is still in the form's fields
        
        """
        form = EventFormAllowsPast()

        self.assertIn('title', form.fields)

    def test_fields_replaced(self):
        """
        Test that time_range replaces both time_start and time_end fields in
        the form 
        
        """
        form = EventFormAllowsPast()
        
        self.assertIn('time_range', form.fields)

        self.assertNotIn('time_start', form.fields)
        self.assertNotIn('time_end', form.fields)

    def test_with_existing_instance(self):
        """
        Test to ensure that a pre-existing instance's time_start and time_end
        values are set as defaults for the time_range field

        """
        form = EventFormAllowsPast(instance=self.event)
        
        self.assertEqual(form.initial['time_range'], 
                        (
                            self.event.time_start, 
                            self.event.time_end
                        )
                    )

    def test_save_commit(self):
        """ Test saving a form to database """
        time_range = time_range_generator(self.tomorrow, self.tomorrow)
        data = {
                'title': 'Test Event',
                'time_range': time_range,
            }

        form = EventFormAllowsPast(data)

        self.assertTrue(form.is_valid())

        event = form.save()
        self.assertIsNotNone(event)
        
        self.assertTrue(Event.objects.filter(pk=event.pk).exists())
    
    def test_save_no_commit(self):
        """ Test saving a form without committing directly to database """
        time_range = time_range_generator(self.tomorrow, self.tomorrow)
        data = {
                'title': 'Test Event',
                'time_range': time_range,
            }

        form = EventFormAllowsPast(data)

        self.assertTrue(form.is_valid())

        event = form.save(commit=False)
        self.assertIsNotNone(event)
        self.assertFalse(Event.objects.filter(pk=event.pk).exists())

        event.save() 
        self.assertTrue(Event.objects.filter(pk=event.pk).exists())

    def test_save_bad_time_range(self):
        """
        Ensure that validations are working on the form for bad time range data 
        
        """
        time_range = time_range_generator(self.today, self.yesterday)
        data = {
                'title': 'Test Event',
                'time_range': time_range,
            }

        form = EventFormAllowsPast(data)

        self.assertFalse(form.is_valid())

    def test_allows_past_time_range(self):
        """
        Ensure that a time_range in the past is still valid.
        
        """
        time_range = time_range_generator(self.yesterday, self.tomorrow)
        data = {
                'title': 'Test Event',
                'time_range': time_range,
            }

        form = EventFormAllowsPast(data)

        self.assertTrue(form.is_valid())


