from weather_predictions import hello
from flask import Flask
import os

application = Flask(__name__)
@application.route('/')
def index():
    endpoint = os.environ['API_ENDPOINT']
    greeting = hello(f'AWS EB! This is the {endpoint} Environment\n\n')
    data = snow_forecast_data('FL')
    return greeting, data 

if __name__ == '__main__':
    application.run(host='127.0.0.1', port=8080, debug=True)