/*******************************************

----------- FITBIT DATA HANDLING -----------

*******************************************/

function getSleepStage(time) {
    // Iterate through each sleep entry
    for (var i = 0; i < sleepData.sleep.length; i++) {
        var levelsData = sleepData.sleep[i].levels.data;

        // Iterate through each data entry within levels
        for (var j = 0; j < levelsData.length; j++) {
            var startTime = levelsData[j].startTime;
            var endTime = levelsData[j].endTime;

            // if time range crosses midnight
            if (compareTimes(endTime, startTime) < 0) {
                // console.log('startTime and endTime cross midnight: ' + startTime + endTime);
                // we just need to confirm that our time is less than endTime
                if (compareTimes(time, endTime) <= 0) {
                    return { value: levelsData[j].level };
                }
            } else {
                // Check if the given time falls within the current sleep level
                if (compareTimes(time, startTime) >= 0 && compareTimes(time, endTime) <= 0) {
                    return { value: levelsData[j].level };
                }
            }
        }
    }

    // Return null if no matching sleep stage is found
    return null;
}

// Function to insert sleep data into HTML
function setSleepData(time) {
    // Check if the container already exists
    var existingSleepDataContainer = document.getElementById('fitbit_sleep_data');
    
    // If it exists, then remove existing container
    if (existingSleepDataContainer) {
        existingSleepDataContainer.remove();
    }

    // Create the container div
    var sleepDataContainer = document.createElement('div');
    sleepDataContainer.setAttribute('class', 'card mb-4 mx-auto');
    sleepDataContainer.setAttribute('id', 'fitbit_sleep_data');
    sleepDataContainer.setAttribute('style', 'width: 50%;');

    // Create the card div
    var sleepDataContainerCard = document.createElement('div');
    sleepDataContainerCard.setAttribute('class', 'card-body text-center');

    // Create the h4 element for sleep stage
    var sleepStageElement = document.createElement('h4');
    sleepStageElement.setAttribute('id', 'sleep_stage');
    
    var selectedSleepStage = getSleepStage(time);
    if (selectedSleepStage) {
        sleepStageElement.textContent = '🛌 ' + selectedSleepStage.value;
    } else {
        sleepStageElement.textContent = '🛌 Not Found'; // Handle the case when no data is found
    }

    // Get the container div and append
    var mainContainer = document.getElementById('side_column');
    sleepDataContainerCard.appendChild(sleepStageElement);
    sleepDataContainer.appendChild(sleepDataContainerCard);
    mainContainer.appendChild(sleepDataContainer);
}

// Function to insert hr data into HTML
function setHrData(time) {
    // Split the time string into hours, minutes, and seconds
    var [hours, minutes, seconds] = time.split(':');

    // Check if seconds is 30 or greater
    if (parseInt(seconds) >= 30) {
        // Increment minutes by one and set seconds to 00
        minutes = ('0' + (parseInt(minutes) + 1)).slice(-2);
    }
    
    // Reset seconds to 00
    var modifiedTime = [hours, minutes, '00'].join(':');

    // Check if the container already exists
    var existingHrDataContainer = document.getElementById('fitbit_hr_data');
    
    // If it exists, remove existing container
    if (existingHrDataContainer) {
        existingHrDataContainer.remove();
    }

    // Create the container div
    var hrDataContainer = document.createElement('div');
    hrDataContainer.setAttribute('class', 'card mb-4 mx-auto');
    hrDataContainer.setAttribute('id', 'fitbit_hr_data');
    hrDataContainer.setAttribute('style', 'width: 50%;');

    // Create the card div
    var hrDataContainerCard = document.createElement('div');
    hrDataContainerCard.setAttribute('class', 'card-body text-center');

    // Create the h4 element for heart rate
    var heartRateElement = document.createElement('h4');
    heartRateElement.setAttribute('id', 'heart_rate');
    
    var selectedHeartRate = hrData.find(entry => entry.time === modifiedTime);
    if (selectedHeartRate) {
        heartRateElement.textContent = '❤️ ' + selectedHeartRate.value;
    } else {
        heartRateElement.textContent = '❤️ Not Found'; // Handle the case when no data is found
    }

    // Get the container div and append
    var mainContainer = document.getElementById('side_column');
    hrDataContainerCard.appendChild(heartRateElement);
    hrDataContainer.appendChild(hrDataContainerCard);
    mainContainer.appendChild(hrDataContainer);
}


/*******************************************

------------- HELPER FUNCTIONS -------------

*******************************************/

// Helper function to compare two time strings
function compareTimes(time1, time2) {
    var parsedTime1 = new Date("2000-01-01T" + time1 + "Z");
    var parsedTime2 = new Date("2000-01-01T" + time2 + "Z");

    return parsedTime1 - parsedTime2;
}

