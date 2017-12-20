# File: datetimepicker/widgets.py
from django import forms 
from django.utils import formats, timezone

DATETIME_FORMAT = '%m/%d/%Y %h:%M %p'


class DateTimeRangeWidget(forms.TextInput):
    template_name = 'datetimepicker/forms/widgets/datetimerange.html'

    def __init__(self, attrs=None, format=DATETIME_FORMAT):
        super().__init__(attrs)
        self.format = format 

    def format_value(self, value):
        now = timezone.now()
        fmt = self.format

        if not value:
            return '{0} - {0}'.format(formats.localize_input(now, fmt))

        return '{} - {}'.format(
                    formats.localize_input(value[0], fmt),
                    formats.localize_input(value[1], fmt),
                )

    class Media:
        css = {
                'all': ('datetimepicker/css/styles.css', ),
            }

        js = (
            '//cdn.jsdelivr.net/momentjs/latest/moment.min.js',
            '//cdn.jsdelivr.net/bootstrap.daterangepicker/2/daterangepicker.js',
            'datetimepicker/js/script.js',
        )


class DateTimeRangeField(forms.BaseTemporalField):
    widget = DateTimeRangeWidget
    input_formats = ['{0} - {0}'.format(DATETIME_FORMAT), ]
    
    default_error_messages = {
        'invalid': _('Enter two date/time pairs.')),
    
    def prepare_value(self, value):
        date_range = []
       
        for date in value:
            if isinstance(date, datetime.datetime):
                date_range.append(to_current_timezone(date))
            else:
                date_range.append(date)

        return date_range
    
    def to_python(self, value):
        if value in self.empty_values:
            return None
        
        return from_current_timezone(result)

    def strptime(self, value, format):
        return datetime.datetime.strptime(value, format)
    

class DateTimeField(BaseTemporalField):
#     widget = DateTimeInput
#     input_formats = formats.get_format_lazy('DATETIME_INPUT_FORMATS')
#     default_error_messages = {
#         'invalid': _('Enter a valid date/time.'),
#     }
# 
#     def prepare_value(self, value):
#         if isinstance(value, datetime.datetime):
#             value = to_current_timezone(value)
#         return value

    def to_python(self, value):
        """
        Validate that the input can be converted to a datetime. Return a
        Python datetime.datetime object.
        """
        if value in self.empty_values:
            return None
        if isinstance(value, datetime.datetime):
            return from_current_timezone(value)
        if isinstance(value, datetime.date):
            result = datetime.datetime(value.year, value.month, value.day)
            return from_current_timezone(result)
        result = super().to_python(value)
        return from_current_timezone(result)

    def strptime(self, value, format):
        return datetime.datetime.strptime(value, format)

