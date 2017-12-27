# File: daterangepicker/forms.py
from django.forms import ModelForm

from daterangepicker.widgets import DateTimeRangeField


class TimeRangedModelForm(ModelForm):
    class Meta:
        # Since time_range isn't actually a field in the model, exclude it from
        # being saved into the new model instance.
        exclude = ['time_range', ]

    def __init__(self, *args, **kwargs):
        super(TimeRangedModelForm, self).__init__(*args, **kwargs)
       
        # Get rid of time_start and time_end fields, if they were accidentally
        # included still.
        self.fields.pop('time_start', None)
        self.fields.pop('time_end', None)
        
        # If we are updating an existing object, make sure the time_range
        # defaults reflect this.
        if 'instance' in kwargs:
            self.fields['time_range'] = DateTimeRangeField(
                            initial=[
                                self.instance.time_start, 
                                self.instance.time_end
                            ]
                        )
        else:
            self.fields['time_range'] = DateTimeRangeField()


    def save(self, commit=True):
        """ 
        Extend saving such that time_start and time_end values are manually
        set in the model instance. 
        
        """
        super(TimeRangedModelForm, self).save(commit=False)

        time_start, time_end = self.cleaned_data['time_range']

        self.instance.time_start = time_start
        self.instance.time_end = time_end
        
        if commit:
            self.instance.save()

        return self.instance

