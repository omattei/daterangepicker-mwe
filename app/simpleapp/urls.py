# File: simpleapp/urls.py

from django.urls import path
from simpleapp import views


app_name = 'simpleapp'
urlpatterns = [
    path('', views.home, name='home'),
    path('new/', views.create_event, name='create_event'),
]
