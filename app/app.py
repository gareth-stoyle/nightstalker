from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def fitbit():
    return render_template("fitbit.html")

if __name__ == '__main__':
    app.run(debug=True)