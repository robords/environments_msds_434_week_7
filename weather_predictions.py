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


def plot_forecast_data(item, forecast_name, percentile='p50'):
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
    percentile = result['Forecast']['Predictions'][percentile]
    value_list = [i['Value'] for i in percentile]
    timestamp = [i['Timestamp'] for i in percentile]
    
    return timestamp, value_list


def list_files_in_s3(bucket, path):
    '''
    Get the list of files from S3
    '''
    
    s3 = boto3.client('s3')
    response = s3.list_objects_v2(
        Bucket=bucket,
        Prefix=path
    )

    most_recent_file_date = max([i['LastModified'] for i in response['Contents']])
    most_recent_file_key = ([i['Key'] for i in response['Contents'] 
                         if i['LastModified'] == most_recent_file_date][0])
    return response, most_recent_file_key


def get_file_from_s3(bucket, path):
    _, key = list_files_in_s3(bucket, path)
    s3 = boto3.client('s3')
    response = s3.get_object(Bucket=bucket, Key=key)
    df = pd.read_csv(response.get('Body'))
    return df

def get_list_of_services():
    bucket = 'cost-management-robords'
    path = 'by_service'
    services = get_file_from_s3(bucket, path)['service']
    services = services.unique()
    service_list = list(services)
    route_list = [f'/costs/{i}' for i in service_list]
    plot_list = [f'/costs/{i}/plot' for i in service_list]

    df = pd.DataFrame(list(zip(service_list, route_list, plot_list)), columns=['Services','Routes', 'Plots'])
    return df
