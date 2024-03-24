/*******************************************

------------ DASHBOARD HANDLING ------------

*******************************************/

// Function to load the video in html.
function loadVideo() {
    var containerDiv = document.getElementById("container");

    // Create the video_container div
    var videoContainerDiv = document.createElement("div");
    videoContainerDiv.id = "video_container";
    videoContainerDiv.style.margin = "10px auto";

    // Create the video element
    var videoElement = document.createElement("video");
    videoElement.id = "my_video";
    videoElement.class = "container";
    videoElement.autoplay = "autoplay";
    videoElement.preload = "preload";

    // Set the src attribute with the video file path
    videoElement.src = "/display/" + videoFilename;

    // Append the video element to the video_container div
    videoContainerDiv.appendChild(videoElement);

    // Append the video_container div to the container div
    containerDiv.appendChild(videoContainerDiv);
}

// Function to create time slider based on hrData start and end times
function createTimeSlider() {
    // Assign max based on the extracted time values
    var max = convertToSeconds(timeRange[1]);

    // if video spans two days the slider should be length max + (start time in seconds - 24 hours in seconds)
    if (timeRangeSpansMulti) {
        max = max + (86400 - convertToSeconds(timeRange[0]))
    } else { // otherwise start time in seconds should be taken from max
        max = max - convertToSeconds(timeRange[0]);
    }

    var selectedTime = timeRange[0];

    // Create the container div
    var sliderContainer = document.createElement('div');
    sliderContainer.setAttribute('id', 'time_slider');
    sliderContainer.setAttribute('class', 'container');

    // Create the input element
    var inputElement = document.createElement('input');
    inputElement.setAttribute('id', 'time_slider_input');
    inputElement.setAttribute('type', 'range');
    inputElement.setAttribute('class', 'form-range');
    inputElement.setAttribute('min', '0');
    inputElement.setAttribute('max', max);
    inputElement.setAttribute('step', 1);
    inputElement.setAttribute('value', '0');

    // Create the paragraph element for selected time
    var selectedTimeHeader = document.createElement('h4');
    selectedTimeHeader.setAttribute('id', 'selected_time');
    selectedTimeHeader.textContent = 'Selected Time: ' + selectedTime;

    // Append the elements to the container
    sliderContainer.appendChild(inputElement);
    sliderContainer.appendChild(selectedTimeHeader);

    // Get the container div
    var mainContainer = document.getElementById('container');

    loadVideo(); // load video above slider

    // Append the container to the main time slider container
    mainContainer.appendChild(sliderContainer);
    
    setHrData(selectedTime);
    setSleepData(selectedTime);
}

// Function to handle time slider control
function timeSliderHandler() {
    // Get the paragraph to display the selected time
    var selectedTimeHeader = document.getElementById('selected_time');

    // Calculate selected time to output based on current seconds and the start time of recording
    var startSeconds = convertToSeconds(timeRange[0]);
    var currentSeconds = parseInt(this.value);
    console.log("startSeconds");
    console.log(startSeconds);
    var totalSecondsToConvert = startSeconds + secondsElapsedSinceVideoStart(currentSeconds);
    var selectedTime = convertToTime(totalSecondsToConvert);

    // Update the paragraph with the selected time
    selectedTimeHeader.textContent = 'Selected Time: ' + selectedTime;

    seekVideo(currentSeconds);

    // if there is no data, these divs can stay on Not Found
    if (hrData.length > 0) {
        setHrData(selectedTime);
    }

    if (sleepData.sleep.length > 0) {
        setSleepData(selectedTime);
    }
}

function seekVideo(seconds) {
        var videoElement = document.getElementById("my_video");
        // Set the current time of the video to the calculated seek time
        videoElement.currentTime = seconds;
}

function handleDateChange() {
    // Get the selected date value
    var selectedDate = dateInput.value;

    if (!isValidDate(selectedDate)) {
        alert('Invalid date input. Please enter a valid date.');
        return; // Exit the function if the date is invalid
    }

    // Update the URL with the new 'date' parameter
    var newUrl = window.location.href.split('?')[0] + '?date=' + encodeURIComponent(selectedDate);

    // Reload the page with the updated URL
    window.location.href = newUrl;
}

function handleInvalidDate() {
    // create an error banner if invalidDate
    var mainContainer = document.getElementById('container');

    // Create a new div element for the error message
    var errorDiv = document.createElement('div');
    errorDiv.className = 'error';
    errorDiv.textContent = "Requested Date Error: Resetting to yesterday's date.";

    // Append the error message to the container
    mainContainer.appendChild(errorDiv);
}

/*******************************************

------------- HELPER FUNCTIONS -------------

*******************************************/
function secondsElapsedSinceVideoStart(currentSeconds) {
    // analyses clip timing to understand how many seconds have elapsed
    // since the video start time.
    console.log("in secondsElapsedSinceVideoStart")
    console.log("currentSeconds")
    console.log(currentSeconds)

    for (i=0; i<length(videoData.clips); i++) {
        let secondsElapsed = 0;
        // start_time & end_time to seconds
        let startTimeSeconds = videoData.clips.i.start_time; // get in seconds!!!
        let endTimeSeconds = videoData.clips.i.start_time; // get in seconds!!!
        secondsElapsed = secondsElapsed + (endTimeSeconds - startTimeSeconds);

        // if secondsElapsed < currentSeconds, got to next clip incrementing the secondsElapsed

        // else secondsElapsed > currentSeconds, find the difference and end time - difference is the time to return?

        // else they are equal, end_time of this clip is the time to return?

    }
}

function convertToTime(totalSeconds) {
    // Calculate hours, minutes, and seconds from the total seconds
    var hours = (Math.floor(totalSeconds / 3600) % 24);
    var remainingSeconds = totalSeconds % 3600;
    var minutes = Math.floor(remainingSeconds / 60);
    var seconds = remainingSeconds % 60;

    // Format the hours, minutes, and seconds as two digits
    var formattedHours = ('0' + hours).slice(-2);
    var formattedMinutes = ('0' + minutes).slice(-2);
    var formattedSeconds = ('0' + seconds).slice(-2);

    // Create and return the time string
    return formattedHours + ':' + formattedMinutes + ':' + formattedSeconds;
}

function convertToSeconds(timeString) {
    // Split the time string into hours, minutes, and seconds
    var [hours, minutes, seconds] = timeString.split(':');

    // Convert hours and minutes to total minutes
    seconds = (hours * 3600) + (minutes * 60) + seconds*1;
    return seconds;
}

//Function to notify user that Fitbit data wasn't found
function noVideoMessage() {
    var errorMessage = document.createElement('h1');
    errorMessage.setAttribute('id', 'no_data_message');
    errorMessage.textContent = 'Video does not exist!';

    // Get the container div and append
    var mainContainer = document.getElementById('container');
    mainContainer.appendChild(errorMessage);
}

function isValidDate(dateString) {
    var regex = /^\d{4}-\d{2}-\d{2}$/; // Assuming YYYY-MM-DD format
    return regex.test(dateString);
}