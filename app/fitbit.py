import requests
import oauth2 as oauth2
import config
from datetime import datetime, timedelta

### Functionality to retrieve hr and acceleromoter data from fitbit API ###
def time_range_spans_multidays(time_range):
    start_time = datetime.strptime(time_range[0], '%H:%M')
    end_time = datetime.strptime(time_range[1], '%H:%M')

    if start_time > end_time:
        return True
    return False

def get_hr_data(date, time_range_spans_multi, time_range=['00:00', '23:59']):
    if time_range_spans_multi:
        # request across two dates
        # reduce one from date 
        date_plus_1 = (datetime.strptime(date, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d') 
        print('requesting hr data for two days:', date, date_plus_1) 
        hr_request = requests.get(
            f'https://api.fitbit.com/1/user/{config.user_id}/activities/heart/date/{date}/{date_plus_1}/1min/time/{time_range[0]}/{time_range[1]}.json',
            headers={'Authorization': 'Bearer ' + config.access_token}
        )
    else:
        # request across one day
        print('requesting hr data for one day:', date)
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
    if time_range_spans_multi:
        # request across two dates
        # add one to date because fitbit considers date of sleep based on endTime
        date_plus_1 = (datetime.strptime(date, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d') 
        print('requesting sleep date for:', date_plus_1)
        sleep_request = requests.get('https://api.fitbit.com/1.2/user/'+config.user_id+f'/sleep/date/{date_plus_1}.json',
                                    headers={'Authorization': 'Bearer ' + config.access_token})
    else:
        # if timespan spans one day, just give for the date requested.
        print('requesting sleep date for:', date)
        sleep_request = requests.get('https://api.fitbit.com/1.2/user/'+config.user_id+f'/sleep/date/{date}.json',
                                    headers={'Authorization': 'Bearer ' + config.access_token})
        
    
    if sleep_request.status_code != 200:
        raise RuntimeError('fitbit api returned request status code:', sleep_request.status_code)
    
    sleep_data = sleep_request.json()
    sleep_data = format_sleep_data(sleep_data)
    # print(sleep_data)
    return sleep_data

# my device appears to not get skin temp data
# def get_skin_temp_data(date, time_range_spans_multi):
#     if time_range_spans_multi:
#         # request across two dates
#         # reduce one from date 
#         date_plus_1 = (datetime.strptime(date, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d') 
#         print('requesting skin temp data for two days:', date, date_plus_1) 
#         skin_temp_request = requests.get(
#             f'https://api.fitbit.com/1/user/{config.user_id}/temp/skin/date/{date}/{date_plus_1}.json',
#             headers={'Authorization': 'Bearer ' + config.access_token}
#         )
#     else:
#         # request across one day
#         print('requesting skin tmep data for one day:', date)
#         skin_temp_request = requests.get(
#             f'https://api.fitbit.com/1/user/{config.user_id}/temp/skin/date/{date}.json',
#             headers={'Authorization': 'Bearer ' + config.access_token}
#         )
        
#     if skin_temp_request.status_code != 200:
#         raise RuntimeError('fitbit api returned request status code:', skin_temp_request.status_code)

#     skin_temp_data = skin_temp_request.json()
#     print(skin_temp_data)
#     return skin_temp_data

def format_time(entry):
    # Rename dateTime to startTime and convert it to time in hh:mm:ss format
    entry["startTime"] = datetime.strptime(entry.pop("dateTime"), "%Y-%m-%dT%H:%M:%S.%f").strftime("%H:%M:%S")
    
    # Calculate endTime using startTime + length of seconds
    start_time = datetime.strptime(entry["startTime"], "%H:%M:%S")
    end_time = start_time + timedelta(seconds=entry["seconds"])
    entry["endTime"] = end_time.strftime("%H:%M:%S")
    
    return entry

# sleep data is assumed to be stages as opposed to FitBit API classic sleep data
def format_sleep_data(sleep_data):
    # Iterate through each sleep entry and update dateTime in levels.data
    for entry in sleep_data["sleep"]:
        if "levels" in entry and "data" in entry["levels"]:
            entry["levels"]["data"] = [format_time(data_entry) for data_entry in entry["levels"]["data"]]
        
        # Remove 'shortData' if present
        if 'shortData' in entry['levels']:
            del entry['levels']['shortData']
    
    return sleep_data