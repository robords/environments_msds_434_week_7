import pandas as pd
import boto3

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
    route_list = [f'<a href="/costs/{i}">' + f"/costs/{i}" + '</a>' for i in service_list]
    plot_list = [f'<a href="/costs/{i}/p90">' + f"/costs/{i}/p90" + '</a>' for i in service_list]

    df = pd.DataFrame(list(zip(service_list, route_list, plot_list)), columns=['Services','JSON', 'Plots'])
    return df

def get_list_of_states():
    bucket = 'raw-weather-data'
    path = 'SNOW'
    locations = get_file_from_s3(bucket, path)['location']
    locations = locations.unique()
    location_list = list(locations)
    route_list = [f'<a href="/states/{i}">' + f"/states/{i}" + '</a>' for i in location_list]
    plot_list = [f'<a href="/states/{i}/p90">' + f"/states/{i}/p90" + '</a>' for i in location_list]

    df = pd.DataFrame(list(zip(location_list, route_list, plot_list)), columns=['Locations','JSON', 'Plots'])
    return df


def get_homepage_locations_list():
    bucket = 'raw-weather-data'
    path = 'SNOW'
    locations = get_file_from_s3(bucket, path)['location']
    locations = locations.unique()
    location_list = list(locations)

    df = pd.DataFrame(list(zip(location_list)), columns=['Locations'])
    return df