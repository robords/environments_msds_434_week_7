from weather_predictions import hello, get_forecast_data, plot_forecast_data, get_list_of_services
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import pyplot as plt
from flask import Flask, jsonify, Response, render_template, request
import os
import io
import numpy as np
plt.rcParams["figure.figsize"] = [7.50, 3.50]
plt.rcParams["figure.autolayout"] = True

application = Flask(__name__)
@application.route('/', methods=['GET'])
def index():
    try:
        endpoint = os.environ['API_ENDPOINT']
    except KeyError: 
        endpoint = 'Local'
    colors = ['Red', 'Blue', 'Black', 'Orange']
    df = get_list_of_services()
    return render_template('test.html', tables=[df.to_html(classes='data')], titles=df.columns.values, colors=colors, environment=endpoint)

@application.route('/states/<some_state>')
def weather_page(some_state):
    data = get_forecast_data(f'{some_state}', "SNOW_FORECAST")
    resp = jsonify(data)
    resp.status_code = 200
    return resp

@application.route('/costs/<service>')
def cost_page(service):
    data = get_forecast_data(f'{service}', "Cost_Forecastv3")
    resp = jsonify(data)
    resp.status_code = 200
    return resp

@application.route('/costs/<service>/plot')
def plot_service(service):
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    xs, ys = plot_forecast_data(f'{service}', "Cost_Forecastv3")
    axis.plot(xs, ys)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@application.route('/print-plot')
def plot_png():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    xs = np.random.rand(100)
    ys = np.random.rand(100)
    axis.plot(xs, ys)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

if __name__ == '__main__':
    application.run(host='127.0.0.1', port=8080, debug=True)