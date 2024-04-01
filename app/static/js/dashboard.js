/*******************************************

------------ DASHBOARD HANDLING ------------

*******************************************/

// Function to load the video in html.
function loadVideo() {
    var mainColumnDiv = document.getElementById("main_column");

    // Create the video_container div
    var videoContainerDiv = document.createElement("div");
    videoContainerDiv.id = "video_container";
    videoContainerDiv.className = "card mx-auto";
    videoContainerDiv.style = "width: fit-content; border: 0;";

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
    mainColumnDiv.appendChild(videoContainerDiv);
    videoElement.addEventListener('timeupdate', function() {
        timeSliderHandler.call({ currentTime: this.currentTime }, 'video');
    });
}

// Function to create time slider based on hrData start and end times
function createTimeSlider() {
    // Assign max based on the extracted time values
    var max = videoData.duration;
    var selectedTime = videoData.clips[1]['start_time'];

    // Create the card div
    var cardDiv = document.createElement('div');
    cardDiv.setAttribute('class', 'card-body text-center');

    // Create the slider div
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

    // Append the elements to the container
    sliderContainer.appendChild(inputElement);
    cardDiv.appendChild(sliderContainer);

    updateTimeDisplay(selectedTime);

    loadVideo(); // load video above slider
    
    // Get the container div
    var videoContainer = document.getElementById('video_container');
    
    // Append the container to the main time slider container
    videoContainer.appendChild(cardDiv);
    
    setHrData(selectedTime);
    setSleepData(selectedTime);
    setTempData(selectedTime);
    setHumidityData(selectedTime);
}

// Function to handle time slider control
function timeSliderHandler(source) {
    // Calculate selected time to output based on current seconds and the start time of recording
    var startSeconds = convertToSeconds(videoData.clips[1]['start_time']);
    // Determine the source of currentSeconds
    var currentSeconds = parseInt(this.currentTime);
    var totalSecondsToConvert = secondsElapsedSinceVideoStart(currentSeconds);
    var selectedTime = convertToTime(totalSecondsToConvert);

    if (source == 'slider') {
        seekVideo(currentSeconds);
    }

    updateTimeDisplay(selectedTime);

    // if there is no data, these divs can stay on Not Found
    if (hrData.length > 0) {setHrData(selectedTime);}
    if (sleepData.sleep.length > 0) {setSleepData(selectedTime);}
    if (tempData) {setTempData(selectedTime);}
    if (humidityData) {setHumidityData(selectedTime);}
}

function updateTimeDisplay(time) {
    var mainColumnDiv = document.getElementById("main_column");

    // Check if the container already exists
    var existingTimeContainer = document.getElementById('selected_time');
    
    // If it exists, then remove existing container
    if (existingTimeContainer) {
        existingTimeContainer.textContent = time;
        return
    }

    // Create the card div for selected time
    var timeCardDiv = document.createElement('div');
    timeCardDiv.setAttribute('class', 'card text-center text-white');
    timeCardDiv.setAttribute('id', 'selected_time_card');

    // Create the paragraph element for selected time
    var selectedTimeHeader = document.createElement('h2');
    selectedTimeHeader.setAttribute('id', 'selected_time');
    selectedTimeHeader.textContent = time;

    // Append the elements to the container
    timeCardDiv.appendChild(selectedTimeHeader);
    mainColumnDiv.appendChild(timeCardDiv);
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
    let secondsElapsed = 0;
    let diff = 0;

    for (i=1; i<=Object.keys(videoData.clips).length; i++) {
        // start_time & end_time to seconds
        let startTimeSeconds = convertToSeconds(videoData.clips[i]['start_time']);
        let endTimeSeconds = convertToSeconds(videoData.clips[i]['end_time']);
        secondsElapsed = secondsElapsed + (endTimeSeconds - startTimeSeconds);
        
        if (secondsElapsed < currentSeconds) {
            continue;
        } else if (secondsElapsed > currentSeconds) {
            diff = secondsElapsed - currentSeconds;
            return endTimeSeconds - diff;
        } else {
            return endTimeSeconds;
        }
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
    errorMessage.setAttribute('class', 'card text-center mx-auto');
    errorMessage.textContent = 'Video does not exist!';

    // Get the container div and append
    var mainContainer = document.getElementById('main_column');
    mainContainer.appendChild(errorMessage);
}

function isValidDate(dateString) {
    var regex = /^\d{4}-\d{2}-\d{2}$/; // Assuming YYYY-MM-DD format
    return regex.test(dateString);
}