import pandas as pd
import boto3
import json

client = boto3.client('forecast')
forecastquery = boto3.client(service_name='forecastquery')

def hello(environment):
    """Return a friendly HTTP greeting."""
    result = f'Hello {environment}'
    return result

def snow_forecast_data(state):
    """Return a friendly HTTP greeting."""

    FORECAST_NAME = "SNOW_FORECAST"

    if FORECAST_NAME in [i['ForecastName'] for i in client.list_forecasts()['Forecasts']]:
        print('Found ARN')
        forecast_arn = ([item for item in client.list_forecasts()['Forecasts'] 
                             if item["ForecastName"] == FORECAST_NAME][0]['ForecastArn'])
        result = forecastquery.query_forecast(
            ForecastArn=forecast_arn,
            Filters={"item_id": state}
        )
    else:
        result = f"Could not find forecast {FORECAST_NAME}"
    
    return result