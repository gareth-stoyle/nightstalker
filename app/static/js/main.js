/******************************************

-------------- MAIN FUNCTION --------------

*******************************************/

console.log("If you're seeing this, html and js are working on flask!");
console.log(requestedDate);
console.log(invalidDate);
console.log(hrData);
console.log(sleepData);
console.log(timeRange);
if (timeRangeSpansMulti) {
    console.log('Time range spans multiple days');
} else {
    console.log('Time range DOES NOT span multiple days');
}

var dateInput = document.getElementById('date');
if (!videoAvailable) {
    noVideoMessage();
} else {
    dateInput.addEventListener('change', handleDateChange);
    if (invalidDate) {
        handleInvalidDate();
    }
    createTimeSlider();
    var timeSlider = document.getElementById('time_slider_input');
    timeSlider.addEventListener('input', timeSliderHandler);
}