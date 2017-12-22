# File: simpleapp/admin.py
from simpleapp.models import Event

from django.contrib import admin


# Register your models here.
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    pass
