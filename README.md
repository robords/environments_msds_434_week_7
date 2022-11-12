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

## Benchmarking

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

__Project Requirements__
* Source code stored in Github
* Continuous Deployment from CircleCI
* Data stored in GCP (BigQuery, Google Cloud Storage, etc.)
* ML predictions created and served out (AutoML, BigQuery, etc.)
* Stackdriver installed for monitoring
* Google App Engine serves out HTTP requests via REST API with a JSON payload
* Deployed into GCP environment
* A two-page, single-spaced paper describing the project as a consultant would describe it to a client during the hand-off phase.


