# File: simpleapp/tests/test_views.py
from django.test import TestCase, Client
from django.urls import reverse

from django.utils import timezone

from simpleapp.models import Event

from daterangepicker.forms import time_range_str

import datetime

HOME_URL = reverse('simpleapp:home')
CREATE_EVENT_URL = reverse('simpleapp:create_event')


class HomeTestCase(TestCase):

    def setUp(self):
        self.tomorrow = timezone.now() + datetime.timedelta(hours=24)
        self.tomorrow_pl1 = timezone.now() + datetime.timedelta(hours=48)
        self.tomorrow_pl2 = timezone.now() + datetime.timedelta(hours=72)
        
        self.events = [
                Event.objects.create(
                        title="Test Event1",
                        time_start=self.tomorrow,
                        time_end=self.tomorrow,
                    ),
                Event.objects.create(
                        title="Test Event2",
                        time_start=self.tomorrow_pl1,
                        time_end=self.tomorrow_pl2,
                    ),
                Event.objects.create(
                        title="Test Event3",
                        time_start=self.tomorrow,
                        time_end=self.tomorrow_pl2,
                    )
            ]

        self.time_ranges = [
                    time_range_str(e.time_start, e.time_end, html=True) 
                    for e in self.events
                ]

    def test_view_events(self):
        """
        Test that all created events are shown on homepage

        """
        client = Client()

        response = client.get(HOME_URL)
        self.assertTemplateUsed(response, 'simpleapp/index.html')
        
        for i, event in enumerate(self.events):
            self.assertContains(response, 
                    '<strong>{}</strong>'.format(event.title))
            self.assertContains(response, self.time_ranges[i])

    def test_view_create_event(self):
        """
        View create event page, but don't post anything

        """
        client = Client()

        response = client.get(CREATE_EVENT_URL)
        self.assertTemplateUsed(response, 'simpleapp/create.html')

    def test_post_create_event(self):
        """
        Actually create an event using the view

        """
        client = Client()
        
        time_range = time_range_str(self.tomorrow, self.tomorrow_pl1)
        data = {
                'title': 'Test Event',
                'time_range': time_range,
            }
        
        response = client.post(CREATE_EVENT_URL, data)
        self.assertTemplateUsed(response, 'simpleapp/create.html')
    
        self.assertContains(response, 
                '<strong>Success!</strong> Event has been created.') 
        self.assertTrue(Event.objects.filter(title='Test Event').exists())

    def test_post_create_even_bad_time(self):
        """
        Send bad data to event creation form and see if an event is created or
        not

        """
        client = Client()

        time_range = time_range_str(self.tomorrow_pl1, self.tomorrow)
        data = {
                'title': 'Test Event',
                'time_range': time_range,
            }
        
        response = client.post(CREATE_EVENT_URL, data)
        self.assertTemplateUsed(response, 'simpleapp/create.html')
   
        self.assertContains(response, 'End date is before start date.')
        self.assertNotContains(response, 
                '<strong>Success!</strong> Event has been created.') 
        self.assertFalse(Event.objects.filter(title='Test Event').exists())




