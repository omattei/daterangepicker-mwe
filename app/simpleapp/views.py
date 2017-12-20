# File: simpleapp/views.py
from simpleapp import forms

from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'simpleapp/index.html')

def create(request):
    form = forms.EventForm()

    return render(request, 'simpleapp/create.html',
                {
                    'form': form,
                }
            )
