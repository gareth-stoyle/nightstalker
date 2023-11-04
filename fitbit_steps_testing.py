import requests
import time
import json
import csv
from pprint import pprint
import oauth2 as oauth2

access_token = 'example'
user_id = 'example'

activity_request = requests.get('https://api.fitbit.com/1/user/'+user_id+'/activities/steps/date/today/today.json',
                                headers={'Authorization': 'Bearer ' + access_token})

print(activity_request.status_code)
pprint(activity_request.json()['activities-steps'])