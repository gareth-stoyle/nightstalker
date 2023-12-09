/*******************************************

------------ DASHBOARD HANDLING ------------

*******************************************/

// Function to create time slider based on hrData start and end times
function createTimeSlider() {
    // Assign min and max based on the extracted time values
    var min = convertToMinutes(timeRange[0]);
    var max = convertToMinutes(timeRange[1]);
    if (timeRangeSpansMulti) {
        max = max + 1440;
    }
    var selectedTime = convertToTime(min);

    // Create the container div
    var sliderContainer = document.createElement('div');
    sliderContainer.setAttribute('id', 'time_slider');
    sliderContainer.setAttribute('class', 'container');

    // Create the input element
    var inputElement = document.createElement('input');
    inputElement.setAttribute('id', 'time_slider_input');
    inputElement.setAttribute('type', 'range');
    inputElement.setAttribute('class', 'form-range');
    inputElement.setAttribute('min', min);
    inputElement.setAttribute('max', max);
    inputElement.setAttribute('step', 1);
    inputElement.setAttribute('value', min);

    // Create the paragraph element for selected time
    var selectedTimeHeader = document.createElement('h4');
    selectedTimeHeader.setAttribute('id', 'selected_time');
    selectedTimeHeader.textContent = 'Selected Time: ' + selectedTime;

    // Append the elements to the container
    sliderContainer.appendChild(inputElement);
    sliderContainer.appendChild(selectedTimeHeader);

    // Get the container div
    var mainContainer = document.getElementById('container');

    // Append the container to the main time slider container
    mainContainer.appendChild(sliderContainer);

    setHrData(timeRange[0]+':00');
    setSleepData(timeRange[0]+':00');
    // setSkinTempData(firstTime);
}

// Function to handle time slider control
function timeSliderHandler() {
    // Get the paragraph to display the selected time
    var selectedTimeHeader = document.getElementById('selected_time');

    // Calculate hours and minutes from the value of the range slider
    var minutes = parseInt(this.value);
    var selectedTime = convertToTime(minutes);

    // Update the paragraph with the selected time
    selectedTimeHeader.textContent = 'Selected Time: ' + selectedTime;

    // add 00 for FitBit HR retrieval
    setHrData(selectedTime+':00');
    setSleepData(selectedTime+':00');
    // setSkinTempData(selectedTime+':00');
}

function handleDateChange() {
    // Get the selected date value
    var selectedDate = dateInput.value;

    // Update the URL with the new 'date' parameter
    var newUrl = window.location.href.split('?')[0] + '?date=' + encodeURIComponent(selectedDate);

    // Reload the page with the updated URL
    window.location.href = newUrl;
}

/*******************************************

------------- HELPER FUNCTIONS -------------

*******************************************/

function convertToTime(minutes) {
    // Calculate hours and minutes from the total minutes
    var hours = (Math.floor(minutes / 60) % 24);
    var remainingMinutes = minutes % 60;

    // Format the hours and minutes as two digits
    var formattedHours = ('0' + hours).slice(-2);
    var formattedMinutes = ('0' + remainingMinutes).slice(-2);

    // Create and return the time string
    return formattedHours + ':' + formattedMinutes;
}

function convertToMinutes(timeString) {
    // Split the time string into hours, minutes, and seconds
    var [hours, minutes, seconds] = timeString.split(':');

    // Convert hours and minutes to total minutes
    var totalMinutes = parseInt(hours) * 60 + parseInt(minutes);

    return totalMinutes;
}

//Function to notify user that Fitbit data wasn't found
function noDataMesage() {
    var errorMessage = document.createElement('h1');
    errorMessage.setAttribute('id', 'no_data_message');
    errorMessage.textContent = 'FitBit Data not found!';

    // Get the container div and append
    var mainContainer = document.getElementById('container');
    mainContainer.appendChild(errorMessage);
}