from weather_predictions import hello, snow_forecast_data
from flask import Flask
from flask import jsonify
import os

application = Flask(__name__)
@application.route('/')
def index():
    try:
        endpoint = os.environ['API_ENDPOINT']
    except KeyError: 
        endpoint = 'Local'
    greeting = hello(f'AWS EB! This is the {endpoint} Environment')
    return greeting

@application.route('/states/<some_state>')
def weather_page(some_state):
    data = snow_forecast_data(f'{some_state}')
    resp = jsonify(data)
    resp.status_code = 200
    return resp

if __name__ == '__main__':
    application.run(host='127.0.0.1', port=8080, debug=True)