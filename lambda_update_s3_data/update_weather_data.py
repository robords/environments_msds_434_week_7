#!/usr/bin/env python
# coding: utf-8

from lambda_update_s3_data import pandas as pd
from lambda_update_s3_data import boto3
import datetime
from collections import defaultdict
from io import StringIO


def get_most_recent_date_from_s3():
    '''
    Here, we get the most recent file from s3, and then get the date from it
    '''
    # Here's the URIs
    bucket = 'raw-weather-data'
    path_names = ['SNOW', 'PRCP', 'SNWD', 'TMAX', 'TMIN']
    
    current_year = datetime.datetime.now().year
    s3 = boto3.client('s3')
    response = s3.list_objects_v2(
            Bucket=bucket,
            Prefix=path_names[0] # this is somewhat arbitrary, but we just need to pick a path
        )

    for item in path_names:
        key = [i['Key'] for i in response['Contents'] if str(current_year) in
              i['Key']][0]
        
    response = s3.get_object(Bucket=bucket, Key=key)
    most_recent_df = pd.read_csv(response.get("Body"))
    most_recent_date_available = most_recent_df['date-'].max()

    return most_recent_date_available


def get_and_put_data_from_noaa(event, context):
    '''
    The NOAA data is organized into yearly files, so all I need to do is overwrite the file
    for the year where we're trying to fill in the gaps
    http://noaa-ghcn-pds.s3.amazonaws.com/csv/1788.csv
    '''
    bucket = 'noaa-ghcn-pds'
    path_name = 'csv.gz'
    
    current_year = datetime.datetime.now().year
    s3 = boto3.client('s3')
    response = s3.list_objects_v2(
            Bucket=bucket,
            Prefix=path_name 
        )

    key = [i['Key']  for i in response['Contents'] if f'/{str(current_year)}.csv.gz' in i['Key']]
    response = s3.get_object(Bucket=bucket, Key=key[0])
    most_recent_df = pd.read_csv(response.get("Body"), compression='gzip', 
                                 names=['id','date-','element','r-eported_value',
                                        'M-FLAG','Q-FLAG','S-FLAG','OBS-TIME'])
    
    # filter out the columns with bad data
    most_recent_df =  most_recent_df[~(most_recent_df['Q-FLAG'].isnull())]
    # combine the file with the stations file to get the states
    stations = pd.read_csv('./stations.csv')
    most_recent_df = most_recent_df.merge(stations, left_on='id', right_on='id')
    most_recent_df.rename(columns={"state": 'location'}, inplace=True)
    # create a separate file for each value in the third column
    df_dict = defaultdict(dict)
    elements = ['PRCP','SNOW','SNWD','TMAX','TMIN']
    for i in elements:
        # filter the dataframe for just the records with that element
        df = most_recent_df[(most_recent_df.element == i)]
        # select only the columns we need:
        df = df[['date-', 'r-eported_value', 'location']]
        # update the date field so it's got dashes
        df['date-'] = pd.to_datetime(df['date-'], format='%Y%m%d') 
        df['date-'] = df['date-'].dt.strftime('%Y-%m-%d')
        # add them to a dict of dataframes
        df_dict[i] = df
        
        # write it directly to s3
        bucket = 'raw-weather-data'
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False)
        s3_resource = boto3.resource('s3')
        s3_resource.Object(bucket, f'{i}/{current_year}.csv').put(Body=csv_buffer.getvalue())






