[![Build Status](https://travis-ci.org/omattei/daterangepicker-mwe.svg?branch=master)](https://travis-ci.org/omattei/daterangepicker-mwe)

# Description
A minimum working example (MWE) for a Django 2.0+ date/time range picker for
use with the Cville Pride events project (currently closed-source).

# License
This project is licensed under the BSD 2-clause "Simplified" License, wherever it
is possible to do so.

Refer to [LICENSE](LICENSE) for more.

# Features

 - `TimeRangedModelForm`, a `ModelForm` subclass that combines two separate
   model fields (`time_start` and `time_end`) into a single form field,
   `time_range`, for easier front-end display.
 - `DateTimeRangeField`, a `MultiValueWidget` subclass that represents the start
   and end of a range of date/times.
 - `DateTimeRangeWidget`, a `TextInput` suclass that provides an interface
   between the interactive [Date Range Picker](http://www.daterangepicker.com/) 
   front-end and the `DateTimeRangeField` class.
 - A very simple app that uses the `TimeRangedModelForm` to create new `Event`
   model instances.

# Pre-requisites
Pre-requisites for this project can be found in [requirements.txt](requirements.txt).

# Credits
This MWE relies on [Date Range Picker](http://www.daterangepicker.com/) for the
front-end display of date ranges. Date Range Picker itself uses
[Bootstrap](https://getbootstrap.com/) and [Moment.js](https://momentjs.com/).
These libraries are included in the `DateTimeRangeWidget`'s `Media` meta class,
which can be loaded in templates via `{{ form.media }}`.
