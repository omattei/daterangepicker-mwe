$(function() {
  $('input[name="time_range"]').daterangepicker({
    timePicker: true,
    timePickerIncrement: 1,
    locale: {
      format: 'MM/DD/YYYY hh:mm A'
    }
  });
});

