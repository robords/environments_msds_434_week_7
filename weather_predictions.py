import pandas as pd
import boto3
from collections import defaultdict

client = boto3.client('forecast', region_name='us-east-1')
forecastquery = boto3.client(service_name='forecastquery', region_name='us-east-1')


def hello(environment):
    """Return a friendly HTTP greeting."""
    result = f'Hello {environment}'
    return result


def get_forecast_data(item, dataset_name, list_of_items):
    """Return the forecast data"""
    if [True for i in client.list_forecasts()['Forecasts'] if dataset_name in i['DatasetGroupArn']][0]:
        print('Found ARN')
        # get the most recent forcast based on the dataset name
        max_creation = max(([i['CreationTime'] for i in client.list_forecasts()['Forecasts']
                             if dataset_name in i['DatasetGroupArn']]))
        forecast_arn = (
        [i['ForecastArn'] for i in client.list_forecasts()['Forecasts'] if dataset_name in i['DatasetGroupArn']
         and i['CreationTime'] == max_creation][0])
        if item == 'all':
            forecast_dict = defaultdict(dict)
            '''
            for i in list_of_items:
                result = forecastquery.query_forecast(
                    ForecastArn=forecast_arn,
                    Filters={"item_id": i}
                )
                percentile_p10 = result['Forecast']['Predictions']['p10']
                forecast_dict['Timestamp'] = [i['Timestamp'] for i in percentile_p10]
                forecast_dict['p10'] = [x + y for x, y in zip(forecast_dict['p10'], [i['Value'] for i in percentile_p10])]
                percentile_p50 = result['Forecast']['Predictions']['p50']
                forecast_dict['p50'] = [x + y for x, y in zip(forecast_dict['p50'], [i['Value'] for i in percentile_p50])]
                percentile_p90 = result['Forecast']['Predictions']['p90']
                forecast_dict['p90'] = [x + y for x, y in zip(forecast_dict['p90'], [i['Value'] for i in percentile_p90])]
            '''
            return "Summary View in WIP"  # forecast_dict
        else:
            result = forecastquery.query_forecast(
                ForecastArn=forecast_arn,
                Filters={"item_id": item}
            )
    else:
        result = f"Could not find forecast for dataset {dataset_name}"

    return result


def plot_forecast_data(item, dataset_name, percentile='p50'):
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
    if item == 'all':
        list_of_items = list(get_homepage_locations_list()['Locations'])
        result = get_forecast_data('all', dataset_name, list_of_items)
        timestamp = result['Timestamp']
        p10 = result['p10']
        p50 = result['p50']
        p90 = result['p90']
        return timestamp, p10, p50, p90
    else:
        result = get_forecast_data(item, dataset_name, '')

        if percentile == 'all':
            percentile_p10 = result['Forecast']['Predictions']['p10']
            timestamp = [i['Timestamp'] for i in percentile_p10]
            p10 = [i['Value'] for i in percentile_p10]
            percentile_p50 = result['Forecast']['Predictions']['p50']
            p50 = [i['Value'] for i in percentile_p50]
            percentile_p90 = result['Forecast']['Predictions']['p90']
            p90 = [i['Value'] for i in percentile_p90]

            return timestamp, p10, p50, p90
        else:
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
    route_list = [
        f'''<button type="button" class="btn btn-success" onclick="location.href='{"costs/" + i}';">Click to view {{JSON}} data</button>'''
        for i in service_list]
    plot_list = [
        f'''<button type="button" class="btn btn-info" onclick="location.href='{"costs/" + i + "/all"}';">Click for Expanded Chart</button>'''
        for i in service_list]

    df = pd.DataFrame(list(zip(service_list, route_list, plot_list)), columns=['Services', 'JSON', 'Plots'])
    return df


def get_list_of_states():
    bucket = 'raw-weather-data'
    path = 'SNOW'
    locations = get_file_from_s3(bucket, path)['location']
    locations = locations.unique()
    location_list = list(locations)
    route_list = [
        f'''<button type="button" class="btn btn-success" onclick="window.open('{"states/" + i}', '_blank');">Click to view {{JSON}} data</button>'''
        for i in location_list]
    plot_list = [
        f'''<button type="button" class="btn btn-info" onclick="window.open('{"states/" + i + "/all"}', '_blank');">Click for Expanded Chart</button>'''
        for i in location_list]

    df = pd.DataFrame(list(zip(location_list, route_list, plot_list)), columns=['Locations', 'JSON', 'Plots'])
    return df


def get_homepage_locations_list():
    bucket = 'raw-weather-data'
    path = 'SNOW'
    locations = get_file_from_s3(bucket, path)['location']
    locations = locations.unique()
    location_list = list(locations)
    json_button_list = [
        f'''<button type="button" class="btn btn-success" onclick="window.open('{"states/" + i}', '_blank');">{{JSON}}</button>'''
        for i in location_list]
    chart_button_list = [
        f'''<button type="button" class="btn btn-info" onclick="window.open('{"states/" + i + "/all"}', '_blank');">Chart</button>'''
        for i in location_list]

    df = pd.DataFrame(list(zip(location_list, json_button_list, chart_button_list)),
                      columns=['Locations', 'View JSON', 'View Chart'])
    return df
