import sys
import os
import json
from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime, timedelta
# to allow for importing of files from ../src
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, '../src')
sys.path.append(src_path)
import fitbit
import video_processing
import db

app = Flask(__name__)


@app.route('/', methods=['GET'])
def dashboard():
    invalid_date = False
    time_range = False
    time_range_spans_multi = False
    hr_data = False
    sleep_data = False
    temp_data = False
    humidity_data = False
    requested_date = request.args.get('date')

    if not requested_date:
        # set to yesterday by default.
        requested_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    if not fitbit.is_valid_date(requested_date):
        invalid_date = True
        requested_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

    video_data = db.retrieve_video(requested_date)

    if video_data:
        time_range = [video_data['start_time'], video_data['end_time']]
        time_range_spans_multi = fitbit.time_range_spans_multidays(time_range)
        hr_data = fitbit.get_hr_data(requested_date, time_range_spans_multi, time_range)
        sleep_data = fitbit.get_sleep_data(requested_date, time_range_spans_multi)
        temp_data = db.retrieve_sensor_entries(requested_date, 'temperature')
        humidity_data = db.retrieve_sensor_entries(requested_date, 'humidity')

    video_filename = video_processing.find_video(requested_date)
    
    print(type(video_data))

    return render_template("dashboard.html", 
                           hr_data=hr_data, 
                           sleep_data=sleep_data,
                           temp_data=temp_data,
                           humidity_data=humidity_data, 
                           requested_date=requested_date,
                           invalid_date=invalid_date,
                           time_range=time_range,
                           time_range_spans_multi=time_range_spans_multi,
                           video_data=video_data,
                           video_filename=video_filename)

	
@app.route('/display/<filename>')
def display_video(filename):
	return redirect(url_for('static', filename='videos/' + filename), code=301)


if __name__ == '__main__':
    app.run(debug=True)
