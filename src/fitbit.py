import requests
import oauth2 as oauth2
import config
from datetime import datetime, timedelta, date

############################
##### HELPER FUNCTIONS #####
############################

def is_valid_date(requested_date):
    """Checks if a given input is a valid date & within an acceptable range"""
    if type(requested_date) != str:
        return False
    try:
        parsed_date = datetime.strptime(requested_date, '%Y-%m-%d').date()

        # Check if the date is before 2020
        if parsed_date.year < 2020:
            return False

        # Check if the date is today or in the future
        today = date.today()
        if parsed_date >= today:
            return False

        return True
    except ValueError:
        return False
    
def time_range_spans_multidays(time_range):
    """Check if a time range spans multiple days."""
    # Error handling for invalid time range format
    if len(time_range) != 2:
        raise ValueError("Invalid time range format. Expected a list with two elements.")

    try:
        start_time = datetime.strptime(time_range[0], '%H:%M:%S')
        end_time = datetime.strptime(time_range[1], '%H:%M:%S')
    except ValueError as e:
        raise ValueError("Invalid time format. Please use the format '%H:%M:%S'.") from e

    return start_time > end_time

# sleep data is assumed to be stages as opposed to FitBit API classic sleep data
def format_sleep_data(sleep_data):
    """Iterates through sleep_data to format the time entries & tidy data"""
    for entry in sleep_data["sleep"]:
        if "levels" in entry and "data" in entry["levels"]:
            entry["levels"]["data"] = [format_time(data_entry) for data_entry in entry["levels"]["data"]]
        
        # Remove 'shortData' if present
        if 'shortData' in entry['levels']:
            del entry['levels']['shortData']
    
    return sleep_data

def format_time(entry):
    """Reformat dateTime & add an endTime in a given sleep_data entry"""
    if "dateTime" not in entry:
            raise ValueError("Missing 'dateTime' field in sleep data entry.")
    try:
        entry["startTime"] = datetime.strptime(entry.pop("dateTime"), "%Y-%m-%dT%H:%M:%S.%f").strftime("%H:%M:%S")

        # Calculate endTime using startTime + length of seconds
        start_time = datetime.strptime(entry["startTime"], "%H:%M:%S")
        end_time = start_time + timedelta(seconds=entry["seconds"])
        entry["endTime"] = end_time.strftime("%H:%M:%S")

        return entry
    
    except ValueError as e:
        raise ValueError(f"Error formatting sleep data entry: {str(e)}")

############################
### FitBit API FUNCTIONS ###
############################

def get_hr_data(date, time_range_spans_multi, time_range=['00:00:00', '23:59:59']):
    """Retrieve heart rate data from Fitbit API for a given date and time range."""

    if time_range_spans_multi:
        # request across two dates
        # reduce one from date 
        date_plus_1 = (datetime.strptime(date, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d') 
        # print('requesting hr data for two days:', date, date_plus_1) 
        hr_request = requests.get(
            f'https://api.fitbit.com/1/user/{config.user_id}/activities/heart/date/{date}/{date_plus_1}/1min/time/{time_range[0]}/{time_range[1]}.json',
            headers={'Authorization': 'Bearer ' + config.access_token}
        )
    else:
        # request across one day
        # print('requesting hr data for one day:', date)
        hr_request = requests.get(
            f'https://api.fitbit.com/1/user/{config.user_id}/activities/heart/date/{date}/1d/1min/time/{time_range[0]}/{time_range[1]}.json',
            headers={'Authorization': 'Bearer ' + config.access_token}
        )
        
    if hr_request.status_code != 200:
        raise RuntimeError('fitbit api returned request status code:', hr_request.status_code)

    hr_data = hr_request.json()['activities-heart-intraday']['dataset']
    # print(hr_data)
    return hr_data

def get_sleep_data(date, time_range_spans_multi):
    """Retrieve sleep data from Fitbit API for given date(s)."""
    if time_range_spans_multi:
        # request across two dates
        # add one to date because fitbit considers date of sleep based on endTime
        date_plus_1 = (datetime.strptime(date, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d') 
        # print('requesting sleep data for:', date_plus_1)
        sleep_request = requests.get('https://api.fitbit.com/1.2/user/'+config.user_id+f'/sleep/date/{date_plus_1}.json',
                                    headers={'Authorization': 'Bearer ' + config.access_token})
    else:
        # if timespan spans one day, just give for the date requested.
        # print('requesting sleep data for:', date)
        sleep_request = requests.get('https://api.fitbit.com/1.2/user/'+config.user_id+f'/sleep/date/{date}.json',
                                    headers={'Authorization': 'Bearer ' + config.access_token})
        
    
    if sleep_request.status_code != 200:
        raise RuntimeError('fitbit api returned request status code:', sleep_request.status_code)
    
    sleep_data = sleep_request.json()
    sleep_data = format_sleep_data(sleep_data)
    # print(sleep_data)
    return sleep_data
