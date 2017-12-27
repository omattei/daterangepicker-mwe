# File: simpleapp/tests/test_forms.py
from django.test import TestCase
from django.utils import timezone
from django.utils.formats import localize_input

from django.forms import ValidationError
from django.forms.utils import to_current_timezone

from simpleapp.models import Event
from simpleapp.forms import EventForm

import datetime

DATETIME_FORMAT = '%m/%d/%Y %I:%M %p'


class EventFormTestCase(TestCase):

    def setUp(self):
        self.today = timezone.now() + datetime.timedelta(minutes=1)
        
        self.yesterday = self.today - datetime.timedelta(hours=24)
        self.tomorrow = self.today + datetime.timedelta(hours=24)
        
        self.form = EventForm()

        self.event = Event.objects.create(
                        title="Test Event",
                        time_start=self.tomorrow,
                        time_end=self.tomorrow,
                    )

    def test_title_still_in_fields(self):
        """
        Test that the title field is still in the form's fields
        
        """
        self.assertIn('title', self.form.fields)

    def test_fields_replaced(self):
        """
        Test that time_range replaces both time_start and time_end fields in the form 
        
        """
        self.assertIn('time_range', self.form.fields)

        self.assertNotIn('time_start', self.form.fields)
        self.assertNotIn('time_end', self.form.fields)

    def test_with_existing_instance(self):
        """
        Test to ensure that a pre-existing instance's time_start and time_end
        values are set as defaults for the time_range field

        """
        form = EventForm(instance=self.event)
        
        self.assertEqual(form.fields['time_range'].fields[0].initial, 
                self.event.time_start)
        self.assertEqual(form.fields['time_range'].fields[1].initial, 
                self.event.time_end)

