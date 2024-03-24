/******************************************

-------------- MAIN FUNCTION --------------

*******************************************/

console.log("If you're seeing this, html and js are working on flask!");
console.log(requestedDate);
console.log(invalidDate);
console.log(hrData);
console.log(sleepData);
console.log(timeRange);
console.log(videoData);
console.log(videoFilename);

console.log(videoData.clips);


if (timeRangeSpansMulti) {
    console.log('Time range spans multiple days');
} else {
    console.log('Time range DOES NOT span multiple days');
}

var dateInput = document.getElementById('date');
dateInput.addEventListener('change', handleDateChange);
    if (invalidDate) {
        handleInvalidDate();
    }
    
if (!videoFilename) {
    noVideoMessage();
} else {
    createTimeSlider();
    var timeSlider = document.getElementById('time_slider_input');
    timeSlider.addEventListener('input', timeSliderHandler);
}
