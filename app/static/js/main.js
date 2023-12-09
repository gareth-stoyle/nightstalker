/******************************************

-------------- MAIN FUNCTION --------------

*******************************************/

console.log("If you're seeing this, html and js are working on flask!");
console.log(requestedDate);
console.log(hrData);
console.log(sleepData);
console.log(timeRange);
if (timeRangeSpansMulti) {
    console.log('Time range spans multiple days');
} else {
    console.log('Time range DOES NOT span multiple days');
}

var dateInput = document.getElementById('date');

// this should be smarter, should be capable of displaying data aslong as footage is provided
// failing gracefully on other data points
dateInput.addEventListener('change', handleDateChange);
if (hrData.length == 0) {
    // handle no hrData
    // console.log('running no data message');
    noDataMesage();
} else {
    // console.log('hr data found');
    createTimeSlider();
    var timeSlider = document.getElementById('time_slider_input');
    timeSlider.addEventListener('input', timeSliderHandler);
}
