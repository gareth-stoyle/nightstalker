console.log("If you're seeing this, html and js are working on flask!");
console.log(hrData);

function convertToTime(minutes) {
    // Calculate hours and minutes from the total minutes
    var hours = Math.floor(minutes / 60);
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

//Function to create time slider based on hrData start and end times
function createTimeSlider() {
    // Extract the first and last time values
    var firstTime = hrData[0].time;
    var lastTime = hrData[hrData.length - 1].time;

    // Assign min and max based on the extracted time values
    var min = convertToMinutes(firstTime);
    var max = convertToMinutes(lastTime);
    var selectedTime = convertToTime(min);

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

    // Get the container div (assuming its ID is "time_slider")
    var timeSliderContainer = document.getElementById('time_slider');

    // Append the elements to the container
    timeSliderContainer.appendChild(inputElement);
    timeSliderContainer.appendChild(selectedTimeHeader);

    setHrData(firstTime);
}

// Function to handle time slider control
function timeSliderHandler() {
    // Get the paragraph to display the selected time
    var selectedTimeHeader = document.getElementById('selected_time');

    // Calculate hours and minutes from the value of the range slider
    var totalMinutes = parseInt(this.value);
    var hours = Math.floor(totalMinutes / 60);
    var minutes = totalMinutes % 60;

    // Format the hours and minutes as two digits
    var formattedHours = ('0' + hours).slice(-2);
    var formattedMinutes = ('0' + minutes).slice(-2);
    var formattedTime = formattedHours + ':' + formattedMinutes + ':00';

    // Update the paragraph with the selected time
    selectedTimeHeader.textContent = 'Selected Time: ' + formattedHours + ':' + formattedMinutes;

    setHrData(formattedTime);
    setAccelData(formattedTime)
}

// Function to insert JSON data into HTML
function setHrData(time) {
    // Get the container element
    var heartRateElement = document.getElementById('heart_rate');

    var selectedHeartRate = hrData.find(entry => entry.time === time);
    if (selectedHeartRate) {
        heartRateElement.textContent = 'Heart Rate: ' + selectedHeartRate.value;
    } else {
        heartRateElement.textContent = 'Heart Rate: Not Found'; // Handle the case when no data is found
    }
}

function setAccelData(time) {
    console.log('placeholder for accelerometer data')
}


createTimeSlider();
var timeSlider = document.getElementById('time_slider_input');
timeSlider.addEventListener('input', timeSliderHandler);

