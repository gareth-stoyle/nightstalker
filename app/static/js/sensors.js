// Functions to insert data into HTML

function setTempData(time) {
    // Convert time to unix timestamp
    var unixTime = getUnixTime(requestedDate, time, plusOne=false);
    var unixTimePlusOne = getUnixTime(requestedDate, time, plusOne=true);

    // Check if the container already exists
    var existingTempDataContainer = document.getElementById('temp_data');
    
    // If it exists, remove existing container
    if (existingTempDataContainer) {
        existingTempDataContainer.remove();
    }

    // Create the container div
    var tempDataContainer = document.createElement('div');
    tempDataContainer.setAttribute('class', 'card mb-4 mx-auto');
    tempDataContainer.setAttribute('id', 'temp_data');
    tempDataContainer.setAttribute('style', 'width: 50%;');


    // Create the card div
    var tempDataContainerCard = document.createElement('div');
    tempDataContainerCard.setAttribute('class', 'card-body text-center');

    // Create the h4 element for temp
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
        tempElement.textContent = '🌡 ' + selectedTemp + '°C';
    } else {
        tempElement.textContent = '🌡 Not Found'; // Handle the case when no data is found
    }

    // Get the container div and append
    var mainContainer = document.getElementById('side_column');
    tempDataContainerCard.appendChild(tempElement);
    tempDataContainer.appendChild(tempDataContainerCard);
    mainContainer.appendChild(tempDataContainer);
}

function setHumidityData(time) {
    // Convert time to unix timestamp
    var unixTime = getUnixTime(requestedDate, time, plusOne=false);
    var unixTimePlusOne = getUnixTime(requestedDate, time, plusOne=true);

    // Check if the container already exists
    var existingHumidityDataContainer = document.getElementById('humidity_data');
    
    // If it exists, remove existing container
    if (existingHumidityDataContainer) {
        existingHumidityDataContainer.remove();
    }

    // Create the container div
    var humidityDataContainer = document.createElement('div');
    humidityDataContainer.setAttribute('class', 'card mb-4 mx-auto');
    humidityDataContainer.setAttribute('id', 'humidity_data');
    humidityDataContainer.setAttribute('style', 'width: 50%;');

    // Create the card div
    var humidityDataContainerCard = document.createElement('div');
    humidityDataContainerCard.setAttribute('class', 'card-body text-center');

    // Create the h4 element for humidity
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
        humidityElement.textContent = '💧 ' + selectedHumidity + '%';
    } else {
        humidityElement.textContent = '💧 Not Found'; // Handle the case when no data is found
    }

    // Get the container div and append
    var mainContainer = document.getElementById('side_column');
    humidityDataContainerCard.appendChild(humidityElement);
    humidityDataContainer.appendChild(humidityDataContainerCard);
    mainContainer.appendChild(humidityDataContainer);
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