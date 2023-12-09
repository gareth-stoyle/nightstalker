from flask import Flask, render_template, request
from datetime import datetime
import fitbit

app = Flask(__name__)

@app.route('/', methods=['GET'])
def dashboard():
    time_range = ['23:25','08:04']
    time_range_spans_multi = fitbit.time_range_spans_multidays(time_range)
    requested_date = request.args.get('date')
    if not requested_date:
        requested_date = datetime.now().strftime('%Y-%m-%d')
    hr_data = fitbit.get_hr_data(requested_date, time_range_spans_multi, time_range)
    sleep_data = fitbit.get_sleep_data(requested_date, time_range_spans_multi)
    # skin_temp_data = fitbit.get_skin_temp_data(requested_date, time_range_spans_multi) not supported on my device it seems

    print('Time Range:', time_range)      
    
    return render_template("dashboard.html", 
                           hr_data=hr_data, 
                           sleep_data=sleep_data,
                        #    skin_temp_data=skin_temp_data, not supported on my device it seems
                           requested_date=requested_date,
                           time_range=time_range,
                           time_range_spans_multi=time_range_spans_multi)

if __name__ == '__main__':
    app.run(debug=True)