import requests
import oauth2 as oauth2
import config

### Functionality to retrieve hr and acceleromoter data from fitbit API ###

def get_hr_data(date, time_range=None):
    hr_request = requests.get('https://api.fitbit.com/1/user/'+config.user_id+f'/activities/heart/date/{date}/1d/1min.json',
                                headers={'Authorization': 'Bearer ' + config.access_token})
    if hr_request.status_code != 200:
        raise RuntimeError('fitbit api returned request status code:', hr_request.status_code)
    hr_data = hr_request.json()['activities-heart-intraday']['dataset']
    if time_range:
        pass
    return hr_data

def get_accel_data(date, time_range='all'):
    pass

hr_data = get_hr_data('2023-11-04')
