from flask import Flask, render_template, request
from datetime import datetime, timedelta
import fitbit

app = Flask(__name__)

@app.route('/', methods=['GET'])
def dashboard():
    invalid_date = False
    video_available = False
    time_range = ['23:25','08:04']
    time_range_spans_multi = fitbit.time_range_spans_multidays(time_range)
    requested_date = request.args.get('date')

    if not requested_date:
        # set to yesterday by default.
        requested_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    if not fitbit.is_valid_date(requested_date):
        invalid_date = True
        requested_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

    hr_data = fitbit.get_hr_data(requested_date, time_range_spans_multi, time_range)
    sleep_data = fitbit.get_sleep_data(requested_date, time_range_spans_multi)
    
    return render_template("dashboard.html", 
                           hr_data=hr_data, 
                           sleep_data=sleep_data,
                           requested_date=requested_date,
                           invalid_date=invalid_date,
                           time_range=time_range,
                           time_range_spans_multi=time_range_spans_multi,
                           video_available=video_available)


if __name__ == '__main__':
    app.run(debug=True)