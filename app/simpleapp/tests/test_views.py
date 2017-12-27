# File: simpleapp/tests/test_views.py
from django.test import TestCase, Client
from django.urls import reverse
from django.conf import settings

from django.utils import timezone
from django.utils.dateformat import format
from django.utils.formats import localize_input

from django.forms.utils import to_current_timezone

from simpleapp.models import Event

import datetime

HOME_URL = reverse('simpleapp:home')
CREATE_EVENT_URL = reverse('simpleapp:create_event')


def time_range_str(start, end, fmt=settings.DATETIME_FORMAT):
    """ Generate time range strings from a given start and end date/time """
    return '{} &ndash; {}'.format(
                format(to_current_timezone(start), fmt),
                format(to_current_timezone(end), fmt),
            )


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
                    time_range_str(e.time_start, e.time_end) 
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

