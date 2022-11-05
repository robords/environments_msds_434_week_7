# get and cleanup the stations file
aws s3 cp s3://noaa-ghcn-pds/ghcnd-stations.txt ./weather/ghcnd-stations.txt
python3 stations_cleanup.py

# upload it
aws s3 cp ./weather/stations.csv s3://raw-weather-data/ghcnd-stations.csv

# Clean up the temp files and directory
rm ./weather/ghcnd-stations.txt