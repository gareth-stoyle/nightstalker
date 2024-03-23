import sys
import os
from flask import Flask, render_template, request, redirect, url_for
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
    requested_date = request.args.get('date')

    if not requested_date:
        # set to yesterday by default.
        requested_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    if not fitbit.is_valid_date(requested_date):
        invalid_date = True
        requested_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

    video_data = db.retrieve_video(requested_date)
    time_range = [video_data['start_time'], video_data['end_time']]
    time_range_spans_multi = fitbit.time_range_spans_multidays(time_range)
    video_filename = video_processing.find_video(requested_date)

    hr_data = fitbit.get_hr_data(requested_date, time_range_spans_multi, time_range)
    sleep_data = fitbit.get_sleep_data(requested_date, time_range_spans_multi)
    
    return render_template("dashboard.html", 
                           hr_data=hr_data, 
                           sleep_data=sleep_data,
                           requested_date=requested_date,
                           invalid_date=invalid_date,
                           time_range=time_range,
                           time_range_spans_multi=time_range_spans_multi,
                           video_date=video_data,
                           video_filename=video_filename)

	
@app.route('/display/<filename>')
def display_video(filename):
	return redirect(url_for('static', filename='videos/' + filename), code=301)


if __name__ == '__main__':
    app.run(debug=True)
