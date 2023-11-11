from flask import Flask, render_template
import fitbit

app = Flask(__name__)

@app.route('/')
def dashboard():
    hr_data = fitbit.get_hr_data('2023-11-04')
    return render_template("dashboard.html", hr_data=hr_data)

if __name__ == '__main__':
    app.run(debug=True)