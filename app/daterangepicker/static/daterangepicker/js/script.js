$(function() {
  $('input[name="date_range"]').daterangepicker({
    timePicker: true,
    timePickerIncrement: 15,
    locale: {
      format: 'MM/DD/YYYY hh:mm A'
    }
  });
});

