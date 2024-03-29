// Functions to insert data into HTML

function setTempData(time) {
    // Convert time to unix timestamp
    var unixTime = getUnixTime(requestedDate, time, plusOne=false);
    var unixTimePlusOne = getUnixTime(requestedDate, time, plusOne=true);
    console.log("Searching for temp data that matches " + Math.floor(unixTime / 100) + " or " + Math.floor(unixTimePlusOne / 100));
    // Check if the container already exists
    var existingTempDataContainer = document.getElementById('temp_data');
    
    // If it exists, remove existing container
    if (existingTempDataContainer) {
        existingTempDataContainer.remove();
    }

    // Create the container div
    var TempDataContainer = document.createElement('div');
    TempDataContainer.setAttribute('class', 'container');
    TempDataContainer.setAttribute('id', 'temp_data');

    // Create the h4 element for heart rate
    var tempElement = document.createElement('h4');
    tempElement.setAttribute('id', 'temp');
    
    var selectedTemp;
    // unix time could be based on requestedDate, or the following day
    for (let key in tempData) {
        if (Math.floor(key / 100) == Math.floor(unixTime / 100)) {
            selectedTemp = tempData[key];
        }
        if (Math.floor(key / 100) == Math.floor(unixTimePlusOne / 100)) {
            selectedTemp = tempData[key];
        }
    }

    if (selectedTemp) {
        tempElement.textContent = 'Temp: ' + selectedTemp;
    } else {
        tempElement.textContent = 'Temp: Not Found'; // Handle the case when no data is found
    }

    // Get the container div and append
    var mainContainer = document.getElementById('container');
    TempDataContainer.appendChild(tempElement);
    mainContainer.appendChild(TempDataContainer);
}

function setHumidityData(time) {
    // Convert time to unix timestamp
    var unixTime = getUnixTime(requestedDate, time, plusOne=false);
    var unixTimePlusOne = getUnixTime(requestedDate, time, plusOne=true);
    console.log("Searching for humidity data that matches " + Math.floor(unixTime / 100) + " or " + Math.floor(unixTimePlusOne / 100));
    // Check if the container already exists
    var existingHumidityDataContainer = document.getElementById('humidity_data');
    
    // If it exists, remove existing container
    if (existingHumidityDataContainer) {
        existingHumidityDataContainer.remove();
    }

    // Create the container div
    var HumidityDataContainer = document.createElement('div');
    HumidityDataContainer.setAttribute('class', 'container');
    HumidityDataContainer.setAttribute('id', 'humidity_data');

    // Create the h4 element for heart rate
    var humidityElement = document.createElement('h4');
    humidityElement.setAttribute('id', 'humidity');
    
    var selectedHumidity;
    // unix time could be based on requestedDate, or the following day
    for (let key in humidityData) {
        if (Math.floor(key / 100) == Math.floor(unixTime / 100)) {
            selectedHumidity = humidityData[key];
        }
        if (Math.floor(key / 100) == Math.floor(unixTimePlusOne / 100)) {
            selectedHumidity = humidityData[key];
        }
    }

    if (selectedHumidity) {
        humidityElement.textContent = 'Humidity: ' + selectedHumidity;
    } else {
        humidityElement.textContent = 'Humidity: Not Found'; // Handle the case when no data is found
    }

    // Get the container div and append
    var mainContainer = document.getElementById('container');
    HumidityDataContainer.appendChild(humidityElement);
    mainContainer.appendChild(HumidityDataContainer);
}

function getUnixTime(requestedDate, timeString, plusOne=false) {
    // Split the time string into hours, minutes, and seconds
    let [hours, minutes, seconds] = timeString.split(':').map(Number);
    let currentDate;

    if (plusOne) {
        currentDate = incrementDateByOneDay(requestedDate);
    } else {
        currentDate = new Date(requestedDate);
    }

    // Set the time components to the requested date
    currentDate.setHours(hours);
    currentDate.setMinutes(minutes);
    currentDate.setSeconds(seconds);

    // Convert the date to Unix time
    let unixTime = currentDate.getTime() / 1000; // Convert milliseconds to seconds

    return unixTime;
}

function incrementDateByOneDay(requestedDate) {
    // Create a new date object initialized with the requested date
    let incrementedDate = new Date(requestedDate);

    // Increment the date by one day
    incrementedDate.setDate(incrementedDate.getDate() + 1);

    return incrementedDate;
}