# File: simpleapp/models.py
from django.db import models


class Event(models.Model):
    """ Represents a named event. """

    title = models.CharField(max_length=100)
    time_start = models.DateTimeField()
    time_end = models.DateTimeField()
