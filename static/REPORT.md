# About this Project

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The National Oceanic and Atmospheric Administration (NOAA) provides a large weather dataset for public consumption, including a time series of different types of precipitation.  The data is available in AWS S3 (https://docs.opendata.aws/noaa-ghcn-pds/readme.html), as well as on Google’s BigQuery.  This project uses the cloud, specifically AWS services. My vision for it was to develop a web page where users could access forecasts I generated using machine learning for the amount of precipitation years in the future for a given geographical area.  The forecasts are presented in two different ways: raw data available in JSON format, as well as charts visualizing the forecast.    

__Architecture:__    

![System Design for Weather Prediction App](/static/msds434_environments.jpg "Architecture")

__GCP Comparative Analysis:__   
 
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The initial plan was to use the Google Cloud Platform (GCP) in this class, but after two weeks, I started to use AWS more often.  The reason for this directly relates to billing and costs. After two weeks of using BigQuery, as I was going through the billing console, I realized that it had racked up three $40 dollar charges while querying the fairly large NOAA dataset and running AutoML and ARIMA time series models on it.  I did not realize this until I had removed the promotional credits from the billing chart, so I began to be concerned about my ability to complete the project and stay under the $300 that was available through the promotion: the queries I had made via BigQuery I intended to keep running, as needed, to complete the project.  The $120 charge was still covered under promotional credit, so my billing alert (set to $25) was not triggered.  I learned later this can be configured, but I was very concerned that I would not get an alert until I owed actual money.  Personally, for a learning experience, I wasn’t comfortable with this.  The final nail in the coffin for using Google Cloud was that I had found a way to process and import data into my model on AWS without incurring charges through a bash script on a low-cost host. I went from paying $40 to query and build the model on Google Cloud to around $7 on AWS, which was a significant improvement from my perspective.  Admittedly, there may have been a similar solution on Google Cloud I could have leveraged: they do have low-cost VMs and Google Cloud Storage, similar to the solution I had implemented on AWS with S3 and EC2.  For both cloud providers, tutorials that describe how to build low-cost alternatives to accomplish tasks embedded within tutorials for high-cost operations, along with the tradeoffs of those alternatives, would be something learners like myself would value because they would provide an opportunity to practice with other services as well as to save money.
Setting costs aside, the technologies I used on AWS vs. that of Google Cloud were very different. I appreciated the simplicity of BigQuery for building models and leveraging AutoML, and the Python SDK allowed me to version control the queries in a language of my choosing.  On AWS, I used Amazon Forecast and S3, moving completely out of the realm of using SQL, though I still was able to take advantage of the Python SDK.  One issue with BigQuery Google was that it didn’t provide feedback on the estimated time for completion for building the forecast with AutoML or ARIMA, while AWS’s Amazon Forecast did.  The lack of insight into completion time contributed to my concerns that I was using vast amounts of resources that I would be billed for later on Google Cloud.  At one point, while waiting on an hours-long model to complete running, I was trying to estimate my costs with the Google Cloud billing calculator, and a very simple mistake where I used the wrong input field estimated my costs in the thousands of dollars, sending me into a panic-driven frenzy to try to find the “cancel” button on the partially completed predictive model. Amazon Forecast gave me predictable results in terms of cost and time for the model to complete. While the barrier for entry for Amazon Forecast can be considered somewhat higher because you cannot simply build the model in one SQL statement, you can choose to fill out multiple forms in the UI, which is arguably even simpler than needing to learn SQL.  However, I do like the flexibility afforded by the Python SDK, where I could pass in variables to my queries, and build a single class to create and update predictions and forecasts on AWS’s service.    

__CI/CD:__   
 
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;I did not use CircleCI for this project.  Instead, I leveraged Github and AWS CodePipeline for the continuous deployment piece. Specifically, in Github, I used Github Actions Pylint.  This provides an analysis of my code for PEP 8 standards compliance, and was incredibly easy to set up.  There are other actions that could reasonably be added.  I’ll note that the Pylint action does not stop my pipeline - I treated the results as stylistic cues, not show-stoppers.  On the topic of pipelines, AWS CodePipeline enabled me to automatically push from my “main” branch repository on Github directly to my beta and main environments.  I leveraged separate branches, i.e. “dev” and “main” in order to build out features and ensure they are working before fetching and merging from dev and then out to my pipeline and web application on Elastic BeanStalk via CodePipeline.      
__Customer-Facing Analysis:__    
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The codebase provides a framework and starting point to iterate further on the use of time-series ML on the cloud and publishing those results to a simple, easy-to-maintain, Flask-based website.  Elastic Beanstalk will scale with demand, and updates from NOAA are predictable enough that S3 and Amazon Forecast costs should also be relatively static each month, even as the predictor is updated periodically.   There are already lots of operational insights and controls in place: monitoring the instances from the Elastic Beanstalk environments through Cloudwatch is enabled, and, as mentioned above, Github Actions enable a wide array of options to enhance testing.  Additional AWS itself, through CodePipelines, provides the ability to add additional testing.    

__Next Steps:__  
   
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Next steps for this system involve adding additional testing and controls into the pipeline and through Github Actions, and building out the data pipeline to provide up-to-date forecasts as new data from NOAA comes in daily.  Specifically, a pipeline needs to be built to update the current year’s file in S3, and I can leverage Amazon Forecasts Python SDK to retrain the predictor on a periodic basis (monthly, to start), similar to what was done here: https://github.com/aws-samples/amazon-forecast-samples/blob/main/notebooks/advanced/Retraining_AutoPredictor/Retraining.ipynb.  Next, Amazon Forecast provides error statistics via the predictor API: for transparency, these should be published to the website on a new path.  On the website itself, a better experience would be to consolidate the charts into the homepage, where they can be loaded via a drop down selector for each state.      
Finally, I should be able to generalize this result to any time-series dataset: the format of the webpage and inputs to build out the forecasts should be able to extended to a generic package where you pass in the input data source, a title (which can be passed to Amazon Forecast to name the dataset, dataset group, predictor and forecast, as well as which can be used on the front end of the website), and a schema for the input data (which is also needed for Amazon Forecast).  To start, I’d require a simple, three column input data source (i.e. the timestamp, value, and an item ID. 


## Helpful commands and More
### Managing Environments

Locally:
* python ./application/application.py

On __Elastic Beanstalk__, there are two environments, beta and prod.
Each are pushed to with _CodePipelines_
* Initialize: eb init
* Create: eb create hello-world
* Change the default environment: eb use hello-world
* Deploy changes: eb deploy
* Open: eb open
* Help: eb -h

__CodePipelines__
Currently, there is a Source, Beta and Prod stages. Any push from Github (Source) automatically pushes those changes 
to the Beta and Prod Elastic Beanstalk environments.

### Benchmarking and logs

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

### Pipeline:
https://aws.amazon.com/getting-started/hands-on/continuous-deployment-pipeline/

# About Me


