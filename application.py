from weather_predictions import hello, get_forecast_data, plot_forecast_data, get_list_of_services
import matplotlib
matplotlib.use('Agg')
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import pyplot as plt
from flask import Flask, jsonify, Response, render_template, request
import os
import io
import numpy as np
import pandas as pd
import seaborn as sns
plt.rcParams["figure.autolayout"] = True

def plot_service(service, percentile):
    fig,ax=plt.subplots(figsize=(14,7))
    ax=sns.set(style="darkgrid")
    xs, ys = plot_forecast_data(f'{service}', "Cost_Forecastv3", percentile)
    df = pd.DataFrame(list(zip(xs, ys)), columns=['date', 'cost'])
    df['date'] = pd.to_datetime(df['date'])
    chart = sns.lineplot(x='date',y='cost', data=df)
    for item in chart.get_xticklabels():
        item.set_rotation(45)
    chart.set(title=f'{service} Forecast')
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

application = Flask(__name__)
@application.route('/', methods=['GET'])
def index():
    try:
        endpoint = os.environ['API_ENDPOINT']
    except KeyError: 
        endpoint = 'Local'
    df = get_list_of_services()
    return render_template('index.html', environment=endpoint)

@application.route('/costs', methods=['GET'])
def costs():
    try:
        endpoint = os.environ['API_ENDPOINT']
    except KeyError:
        endpoint = 'Local'
    df = get_list_of_services()
    return render_template('costs.html', tables=[df.to_html(classes='highlight striped',
                                                            index=False)],
                           #titles=df.columns.values,
                           environment=endpoint)

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

@application.route('/costs/<service>/p50')
def plot_service_p50(service):
    return plot_service(service, 'p50')

@application.route('/costs/<service>/p10')
def plot_service_p10(service):
    return plot_service(service, 'p10')

@application.route('/costs/<service>/p90')
def plot_service_p90(service):
    return plot_service(service, 'p90')

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