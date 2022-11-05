for VARIABLE in 2010 2011 2012 2013 2014 2015 2016 2018 2019 2020 2021 2022; do
    # Get the file
    aws s3 cp s3://noaa-ghcn-pds/csv.gz/"$VARIABLE".csv.gz ./weather/"$VARIABLE".csv.gz
    # Decompress the zip file into a temp directory
    gzip -d ./weather/"$VARIABLE".csv.gz
    # Add headers
    { echo 'id,date,element,value,M-FLAG,Q-FLAG,S-FLAG,OBS-TIME'; cat ./weather/"$VARIABLE".csv; } > ./weather/"$VARIABLE"_with_headers.csv
    # filter out the columns with bad data
    awk -F '","'  'BEGIN {OFS=","} { if ((toupper($6) == ""))  print }' ./weather/"$VARIABLE"_with_headers.csv > ./weather/"$VARIABLE"_filtered.csv
    # create a separate file for each value in the third column
    awk -v year=$VARIABLE -F ',' '{print >> ("./weather/" year "/" $3 ".csv")}' ./weather/"$VARIABLE"_filtered.csv
    # Combine the stations data in and add headers back to the remaining files
    for ELEMENT in PRCP SNOW SNWD TMAX TMIN; do
        {
            join -t, <(sort ./weather/"$VARIABLE"/"$ELEMENT".csv) <(sed 1d ./weather/stations.csv | sort)
        } > ./weather/"$VARIABLE"/"$ELEMENT"_combined.csv
        {
            echo 'id,date,element,reported_value,M-FLAG,Q-FLAG,S-FLAG,OBS-TIME,location'; cat ./weather/"$VARIABLE"/"$ELEMENT"_combined.csv;
        } > ./weather/"$VARIABLE"/"$ELEMENT"_with_headers.csv
        {
            cut -d , -f2,4,9 < ./weather/"$VARIABLE"/"$ELEMENT"_with_headers.csv;
        } > ./weather/"$VARIABLE"/"$ELEMENT"_cut.csv
        # Dates need dashes in them
        sed -r 's/^(.{4})(.{2})/\1-\2-/;s/$//' ./weather/"$VARIABLE"/"$ELEMENT"_cut.csv > ./weather/"$VARIABLE"/"$ELEMENT"_edited.csv
        # Sync up the contents of the temp directory to S3 prefix
        aws s3 cp ./weather/"$VARIABLE"/"$ELEMENT"_edited.csv s3://raw-weather-data/"$ELEMENT"/"$VARIABLE".csv
    done
    # delete all files except those with _with_headers.csv
    ls -d -1 "$PWD/weather/$VARIABLE/"*.* | egrep -v "_edited.csv" | xargs rm
    # Clean up the temp files and directory
    rm ./weather/"$VARIABLE"_with_headers.csv ./weather/"$VARIABLE".csv*
done