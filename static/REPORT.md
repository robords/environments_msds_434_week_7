# About this Project

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The National Oceanic and Atmospheric Administration (NOAA) provides a large weather dataset for public consumption, including a time series of different types of precipitation.  The data is available in AWS S3 (https://docs.opendata.aws/noaa-ghcn-pds/readme.html), as well as on Google’s BigQuery.  This project uses AWS services for ETL, ML, and hosting the web app (see Appendix A for an overview of the different components). My vision for it was to develop a web page where users could access forecasts I generated using machine learning to predict future amounts of precipitation for a given geographical area.  The forecasts are presented in two different ways: raw data available in JSON format, as well as charts visualizing the forecast.

__Architecture:__    

![System Design for Weather Prediction App](/static/msds434_environments.jpg "Architecture")

__GCP Comparative Analysis:__   
 
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; The initial plan was to use the Google Cloud Platform (GCP) in this class, but after two weeks, I started to switch to AWS.  The reason for this relates to billing and costs. After two weeks of using BigQuery, as I was going through the billing console, I realized that it had racked up three $40 dollar charges while querying the fairly large NOAA dataset and running AutoML and ARIMA time series models on it.  I did not realize this until I had removed the promotional credits from the billing chart, so I began to be concerned about my ability to complete the project and stay under the $300 that was available through the promotion: the queries I had made via BigQuery I intended to keep running, as needed, to complete the project and keep the forecast updated as new data came in from NOAA.  The ~$120 charge was still covered under promotional credit, so my billing alert (set to $25) was not triggered.  I learned later this can be configured, but was very concerned that I would not get an alert until I owed actual money.  Personally, for a learning experience, I wasn’t comfortable with this.  The final nail in the coffin for using Google Cloud was that I had found a way to process and import data into my model on AWS without incurring significant charges through a bash script on a low-cost VM. I went from paying $40 to query and build the model on Google Cloud to around $7 on AWS, which was a significant improvement from my perspective.  Admittedly, there may have been a similar solution on Google Cloud I could have leveraged: they do have low-cost VMs and Google Cloud Storage, similar to the solution I had implemented on AWS with S3 and EC2.  For both cloud providers, tutorials that describe how to build low-cost alternatives to accomplish tasks embedded within tutorials for high-cost operations, along with the tradeoffs of those alternatives, would be something learners like myself would value: they would provide an opportunity to practice with other services as well as mitigating fears about incurring large bills at the end of the month.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Setting costs aside, the technologies I used on AWS vs. Google Cloud were very different. I appreciated the simplicity of BigQuery for building models and leveraging AutoML, and the Python SDK allowed me to version control the queries in a language of my choosing.  On AWS, I used Amazon Forecast and S3, moving completely out of the realm of using SQL, though I still was able to take advantage of the AWS Python SDK.  One issue with BigQuery Google was that it didn’t provide feedback on the estimated time for completion for building the forecast with AutoML or ARIMA, while AWS’s Amazon Forecast did.  The lack of insight into completion time contributed to my concerns that I was using vast amounts of resources that I would be billed for later on Google Cloud.  At one point, while waiting on an hours-long model to complete running, I was trying to estimate my costs with the Google Cloud billing calculator, and a very simple mistake where I used the wrong input field estimated my costs in the thousands of dollars, sending me into a panic-driven frenzy to try to find the “cancel” button on the partially completed predictive model. Amazon Forecast gave me predictable results in terms of cost and time for the model to complete. While the barrier for entry for Amazon Forecast may be somewhat higher because you cannot simply build the model in one SQL statement, you can choose to fill out multiple forms in the UI, which is arguably even simpler than needing to learn BigQuery SQL.  However, I do like the flexibility afforded by the Python SDK, where I could pass variables to my queries, and build a single class to create and update predictions and forecasts on AWS’s service.    

__CI/CD:__   
 
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; I leveraged Github and AWS CodePipeline for continuous deployment. Specifically, in Github, I used Github Actions Pylint.  This provides an analysis of my code for PEP 8 standards compliance, and was incredibly easy to set up.  There are other actions that could reasonably be added.  The Pylint Github Action does not stop the pipeline - the results are mostly stylistic cues, not show-stoppers.  On the topic of pipelines, AWS CodePipeline enabled me to automatically push from my “main” branch repository on Github directly to my beta and main Elastic Beanstalk environments, which I used to host the Flask App for this project.  I leveraged separate branches, i.e. “dev” and “main”, in order to build out features and test them, before fetching and merging from dev to the prod branch and then out to my pipeline and web application on Elastic BeanStalk via CodePipeline.  

__Customer-Facing Analysis:__    
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The codebase provides a framework and starting point to iterate further on the use of time-series ML on the cloud and publishing those results to a simple, easy-to-maintain, Flask-based website.  Elastic Beanstalk will scale with demand, and updates from NOAA are predictable enough that S3 and Amazon Forecast costs will also be relatively static each month, even as the predictor algorithm is updated periodically.   There are already lots of operational insights and controls in place: monitoring the instances from the Elastic Beanstalk environments through Cloudwatch is enabled, and, as mentioned above, Github Actions enable a wide array of options to enhance testing beyond linting.  Additionally CodePipelines provides the ability to add additional testing stages, if we wanted to bring something like Jenkins into the mix.

__Next Steps:__  
   
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; To make this package a turn-key system, I’d like to update it to use CDK (AWS’s Cloud Development Kit) to build out the infrastructure with a simple command (i.e. “cdk deploy”).  The reason for this is because while the Python SDK was used quite a bit for Amazon Forecast and S3, the buckets themselves, the Glue Job for ETL, and IAM permissions are all built through the console. While I can document these steps to remember them in the future, CDK allows all of this to be automated. 
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; In terms of features, maintainability and testing, this system needs additional testing and controls built into the pipeline and through Github Actions, and automation needs to be added to provide up-to-date forecasts as new data from the cost dataset.  Specifically, while I have ETL through AWS Glue for copying and transforming data daily as it comes in from NOAA, a Lambda or AWS Glue job needs to be added to automatically retrain the weather predictor on a periodic basis (monthly, to start), as well as a separate job needs to be added to update the Forecast itself.  To clarify, Amazon Forecast calls the model that gets trained the “predictor”, and the forecast built from this predictor the “forecast”.  Users can leverage the same predictor while updating the data for the forecast so as to keep it up to date: this is less expensive than training a new predictor each time.  Next, Amazon Forecast provides error statistics via the predictor API: for transparency, these should be published to the website on a new path for the weather data.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Finally, I’d like to prioritize investigating alternative ETL solutions that are more cost-effective.  AWS Glue gets the job done, but is expensive, especially because the current job requires 1 DPU.  Building the script into a Docker container and deploying it via a lower-cost, dedicated VM may be more cost effective. Alternatively, Elastic Container Service may also be cheaper, as described here: https://www.taloflow.ai/blog/aws-glue-to-ecs.


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



