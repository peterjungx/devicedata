from flask import Flask, send_from_directory, request
import random
import json, os
from socket import gethostname
from readdb import devices, hours_in_day, days_in_week, days_in_month

app = Flask(__name__, static_url_path='/client/public')

# Path for our main Svelte page
@app.route("/")
def base():
    return send_from_directory('client/public', 'index.html')

# Path for all the static files (compiled JS/CSS, etc.)
@app.route("/<path:path>")
def home(path):
    return send_from_directory('client/public', path)


@app.route("/devices")
def devs():
    return devices()

@app.route("/hoursInDay")
def hoursInDay():
    device = request.args.get('device')
    print('device', device)
    tabname = 'd_' + device.split('-')[0]
    day = request.args.get('day')
    return hours_in_day(tabname, day)

@app.route("/daysInWeek")
def daysInWeek():
    device = request.args.get('device')
    tabname = 'd_' + device.split('-')[0]
    day = request.args.get('day')
    return days_in_week(tabname, day)

@app.route("/daysInMonth")
def daysInMonth():
    device = request.args.get('device')
    tabname = 'd_' + device.split('-')[0]
    day = request.args.get('day')
    return days_in_month(tabname, day)

# Tests Python Flask Svelte connection
@app.route("/randData")
def randData():
    params = request.args.get('params')
    randomNumber = random.randint(0, 100)

    data = json.dumps({
        "randomNumber": str(randomNumber), 
        "params": str(int(params)), 
        "sumRandomParams": str(randomNumber + int(params))
        })
    
    return data

if __name__ == "__main__":
    app.run(debug=True, host=gethostname(), port=int(os.environ.get('PORT', 8090)))