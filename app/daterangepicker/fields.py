# File: daterangepicker/fields.py
from django.forms import ValidationError
from django.forms.fields import DateTimeField, MultiValueField

from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from daterangepicker.utils import DATETIME_INPUT_FORMAT
from daterangepicker.widgets import DateTimeRangeWidget


class DateTimeRangeField(MultiValueField):
    widget = DateTimeRangeWidget

    def __init__(self, initial=None, allow_past=False, **kwargs):
        if initial is None:
            initial = (None, None)

        if len(initial) != 2:
            raise ValueError(
                _("Initial data tuple was expected to have " + " exactly two dates.")
            )

        fields = (
            DateTimeField(
                initial=initial[0], input_formats=[DATETIME_INPUT_FORMAT,], **kwargs,
            ),
            DateTimeField(
                initial=initial[1], input_formats=[DATETIME_INPUT_FORMAT,], **kwargs,
            ),
        )

        super(DateTimeRangeField, self).__init__(fields, initial=initial, **kwargs)

        # Allow a time_range to be in the past
        self.allow_past = allow_past

    def clean(self, time_range_str):
        try:
            time_range_tokens = time_range_str.split(" - ")

            start_time_str, end_time_str, *extra = time_range_tokens

            if extra:
                raise ValidationError(_("Expected exactly two dates."))

        except ValueError:
            raise ValidationError(_("Expected more than one date."))

        start_time, end_time = super(DateTimeRangeField, self).clean(
            (start_time_str, end_time_str)
        )

        # Validate that a range of two date/times makes logical sense.
        if end_time < start_time:
            raise ValidationError(_("End date is before start date."))

        if not self.allow_past:
            now = timezone.now().replace(microsecond=0, second=0)

            # Validate that a range of two date/times is not in the past.
            if start_time < now:
                raise ValidationError(_("Start date is in the past."))

        return start_time, end_time

    def compress(self, data_list):
        try:
            start_time, end_time, *extra = data_list
        except (KeyError, ValueError):
            raise ValidationError(_("Expected two valid dates."))

        if extra:
            raise ValidationError(_("Expected exactly two dates."))

        return start_time, end_time
