# File: simpleapp/views.py
from simpleapp import forms
from simpleapp.models import Event

from django.shortcuts import render


# Create your views here.
def home(request):
    events = Event.objects.all()

    return render(request, 'simpleapp/index.html',
                {
                    'events': events,
                }
            )


def create_event(request):
    form = forms.EventForm(request.POST or None)
    created = False

    if request.method == 'POST':
        if form.is_valid():
            created = True
            form.save()
            
    return render(request, 'simpleapp/create.html',
                {
                    'form': form,
                    'created': created,
                }
            )
