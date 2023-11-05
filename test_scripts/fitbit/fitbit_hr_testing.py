import requests
from pprint import pprint
import oauth2 as oauth2
import config


hr_request = requests.get('https://api.fitbit.com/1/user/'+config.user_id+'/activities/heart/date/2023-11-04/1d/1min.json',
                                headers={'Authorization': 'Bearer ' + config.access_token})

print(hr_request.status_code)
pprint(hr_request.json())
pprint(hr_request.json()['activities-heart-intraday']['dataset'])
data = hr_request.json()['activities-heart-intraday']['dataset']

for line in data:
    print(line['value'])