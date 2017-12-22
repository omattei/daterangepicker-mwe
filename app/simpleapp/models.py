# File: simpleapp/models.py
from django.db import models


# Create your models here.
class Event(models.Model):
    title = models.CharField(max_length=100)
    time_start = models.DateTimeField()
    time_end = models.DateTimeField()
