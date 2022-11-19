# Managing Environments

Create a production and development environment and deploy your final project to both environments.

Locally:
* python ./application/application.py

On AWS:
* Initialize: eb init
* Create: eb create hello-world
* Change the default environment: eb use hello-world
* Deploy changes: eb deploy
* Open: eb open
* Help: eb -h

## Benchmarking and logs

__Logs__    
https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/AWSHowTo.cloudwatchlogs.html

__Benchmarking__    
On Mac, Apache Benchmarking is installed by default.  Check it out:

`ab -h`

Example:
`ab -k -n 100 -c 10 http://127.0.0.1:8080/`

* The -k parameter uses the “HTTP KeepAlive Feature”.
* The -n parameter sets the request count (100 in this case).
* The -c parameters sets the concurrent request count.
* We performed the test on our local host

## Pipeline:
https://aws.amazon.com/getting-started/hands-on/continuous-deployment-pipeline/

### Final Project Overview
The final project consists of building a cloud-native analytics application that is hosted on the Google Cloud Platform (GCP). The goal of this project is to give you the ability to create realistic, working solutions that were created with modern techniques.

Before you begin, read the Sculley et al. (2015) paper to consider technical debt in machine-learning (ML) systems. Access the Sculley et al. (2015) reading through Course Reserves.

Project Selection
A project can use public data from Google BigQuery DatasetLinks to an external site. if using BigQuery as the database.  

Alternately, if using AutoML, data can be tutorial data or custom dataLinks to an external site..

The main idea is for you to think about starting to create a portfolio.

### Lambda    
Automatically pushes to S3 when updated in source code (specifically the zip file)    
https://docs.aws.amazon.com/lambda/latest/dg/python-package.html

S3 URL:
https://lambda-for-updating-raw-weather-data.s3.amazonaws.com/lambda_update_s3_data/lambda_update_s3_data.zip