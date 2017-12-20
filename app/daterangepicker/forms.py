# File: datetimepicker/forms.py
from django.forms import ModelForm, ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from datetimepicker.widgets import DateTimeRangeField
import dateutil.parser


class TimeRangedModelForm(ModelForm):
    time_range = DateTimeRangeField()
    exclude = ['time_start', 'time_end']

    def __init__(self, *args, **kwargs):
        super(TimeRangedModelForm, self).__init__(*args, **kwargs)
        
        instance = kwargs.get('instance', None)
        if instance:
            self.fields['time_range'].initial = [
                        instance.time_start, 
                        instance.time_end,
                    ]

    def clean(self):
        """ 
        Perform custom validation on 'time_start' and 'time_end' fields.

        """
        time_range = self.cleaned_data['time_range'].split(' - ')

        if len(time_range) != 2:
            raise ValidationError(_("Expected exactly two dates."))
        
        start_time, end_time = [dateutil.parser.parse(t.strip()) for t in time_range]
        now = timezone.now()

        if start_time and end_time:
            if start_time < now:
                raise ValidationError(_("Start date is in the past."))

            if end_time < now:
                raise ValidationError(_("End date is in the past."))

            if end_time < start_time:
                raise ValidationError(_("End date is before start date."))

        super(TimeRangedModelForm, self).clean()

        return self.cleaned_data

