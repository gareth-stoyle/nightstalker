import requests
import time
import json
import csv
from pprint import pprint
import oauth2 as oauth2

access_token = 'example'
user_id = 'example'

hr_request = requests.get('https://api.fitbit.com/1/user/'+user_id+'/activities/heart/date/today/today.json',
                                headers={'Authorization': 'Bearer ' + access_token})

print(hr_request.status_code)
pprint(hr_request.json())
pprint(hr_request.json()['activities-heart-intraday']['dataset'])
data = hr_request.json()['activities-heart-intraday']['dataset']

for line in data:
    print(line['value'])