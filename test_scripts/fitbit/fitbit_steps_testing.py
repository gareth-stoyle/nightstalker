import requests
from pprint import pprint
import oauth2 as oauth2
import app.config as config

activity_request = requests.get('https://api.fitbit.com/1/user/'+config.user_id+'/activities/steps/date/2023-11-04/1d/1min.json',
                                headers={'Authorization': 'Bearer ' + config.access_token})

print(activity_request.status_code)
pprint(activity_request.json()['activities-steps'])