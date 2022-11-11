import pandas as pd
import boto3
import json

client = boto3.client('forecast', region_name='us-east-1')
forecastquery = boto3.client(service_name='forecastquery', region_name='us-east-1')

def hello(environment):
    """Return a friendly HTTP greeting."""
    result = f'Hello {environment}'
    return result

def get_forecast_data(item, forecast_name):
    """Return the forecast data"""

    FORECAST_NAME = forecast_name #"SNOW_FORECAST"

    if FORECAST_NAME in [i['ForecastName'] for i in client.list_forecasts()['Forecasts']]:
        print('Found ARN')
        forecast_arn = ([item for item in client.list_forecasts()['Forecasts'] 
                             if item["ForecastName"] == FORECAST_NAME][0]['ForecastArn'])
        result = forecastquery.query_forecast(
            ForecastArn=forecast_arn,
            Filters={"item_id": item}
        )
    else:
        result = f"Could not find forecast {FORECAST_NAME}"
    
    return result


def plot_forecast_data(item, forecast_name):
    """Return the forecast data in chart format
    {
      "Forecast": {
        "Predictions": {
          "p10": [
            {
              "Timestamp": "2022-09-08T00:00:00", 
              "Value": -1.2800201246720988e-05
            }, 
    """

    result = get_forecast_data(item, forecast_name)
    p50 = result['Forecast']['Predictions']['p50']
    value_list = [i['Value'] for i in p50]
    timestamp = [i['Timestamp'] for i in p50]
    
    return timestamp, value_list