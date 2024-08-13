# NYC-Taxis
Project 4

## Introduction

For this project, we analyzed Uber trips taken in NYC for all of 2023. This data was pulled from the official NYC database provided by the NYC Taxi and Limousine Commission (TLC), which contains trip records for nearly 15 years (https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page). In particular, we were interested in analyzing the Uber trips, located in the High Volume For-Hire Vehicle (FHV) Trip Data, pulled from NYC OpenData (https://data.cityofnewyork.us/Transportation/2023-High-Volume-FHV-Trip-Data/u253-aew4/about_data).

This dataset contains a row for each trip taken by FHV's in 2023. This includes Uber, Lyft, Via, and Juno. In effort to reduce the number of data points to observed, we limited to Uber data. This allowed us to get a focused dataset for one of the most popular forms of taxis in the city. The trip data is comprehensive, containing fields such as pickup and dropoff locations (based on the TLC Taxi Zone), base passenger fare, tips, trip time and miles, tax, and total driver pay to name a few.

We created 3 supervised machine learning models to find if the data would be able to predict the base passenger fare using various features. To this end, we utilized a frontend HTML and JavaScript, and connected the data from python via Flask API.

## Process

### 1. Extract, Transform, Load
Upon identifying the data as too large to analyze, we sought to reduce the dataset to a manageable, random sample. We utilized Databricks, a cloud-based platform, to store and process large amounts of data. The FHV Trip Data was split per month and stored in parquet files. The parquet files were uploaded to Databricks and read using Spark. The combined Spark dataframe was filtered to extract only Uber trips. A representative random sample was used to reduce runtimes and resources needed for data manipulation and machine learning modeling.


### 2. Creating visualizations


### 3. Configuring the Flask API and the frontend
In order to reduce the runtime from the frontend, we decided to run our data via the backend python file and exporting Flask endpoints to JavaScript. Particularly, this meant saving the plots as PNG's .....


## Machine Learning Model Overview:

### 1. Linear regression
Fits a linear model with coefficients w = (w1, …, wp) to minimize the residual sum of squares between the observed targets in the dataset, and the targets predicted by the linear approximation.

### 2. Random forest regressor
Fits a number of decision tree regressors on various sub-samples of the dataset and uses averaging to improve the predictive accuracy and control over-fitting.  <br />
Step 1. Create a bootstrapped dataset  <br />
Step 2. Create decision tree using the bootstrapped dataset using a random subset of variables at each step  <br />
Step 3. Use aggregate of outcomes to make a decision based on input variables (bagging). 

### 3. Neural networks

## Results
### Data Exploration
* Dataset Dimensions: 1,670,353 rows and 19 columns.
* Column Names: 'DOLocationID', 'PULocationID', 'hvfhs_license_num', 'request_datetime', 'trip_miles', 'trip_time', 'base_passenger_fare', 'tolls', 'bcf', 'sales_tax', 'congestion_surcharge', 'airport_fee', 'tips', 'driver_pay', 'date', 'PUBorough', 'PUZone', 'DOBorough', 'DOZone'.
* Missing Values: 64 in PUBorough, 67,615 in DOBorough.
* Uber Availability: Remained relatively stable each month with minor fluctuations.
* Base Passenger Fare: Gradual increase each month; possibly influenced by factors other than Uber availability, such as demand or operating costs.
* Trip Miles: Remained relatively stable throughout the year.
* Trip Time: Slight increase over the year; longer trip durations may have contributed to the rise in base passenger fare.
* Variability in Trip Time: Significant variability with a higher range and more outliers; distribution skewed to the right with most trips under 50 minutes.
* Congestion Surcharge Distribution: Most common values are 0.0 and 2.75; higher surcharges are rare.
* Tips Distribution: Most tips are between $0 and $10, with few exceeding $20.
* Pairplot Insights: Trip distance and time significantly influence base passenger fare; strong positive correlations among variables.
* Correlation Analysis:
  * Strong Correlation: Base passenger fare and driver pay; trip miles and trip time.
  * Moderate Correlation: Tolls, sales tax, and congestion surcharge with fares and driver pay.
  * Weak Correlation: DOLocationID and PULocationID have minimal impact on other variables.
  * Negative Values: Small percentages of negative values in driver_pay (0.0023%) and base_passenger_fare (0.0402%); should not be allowed in financial transactions.
* Optimal Clusters: 4 clusters based on the Elbow Method.
  * Cluster Insights:
    * Cluster 0: Short, inexpensive trips.
    * Cluster 1 & 2: Moderate trips with some overlap. Overlap between clusters indicated most trips are short with low fares.
    * Cluster 3 captured rare, long, high-cost trips. Long, expensive trips with higher tolls and driver pay.
    * Cluster Centroids: Distinct characteristics for each cluster in terms of trip miles, time, base fare, driver pay, and tolls.

### Machine Learning Model 1. Linear Regression vs Random Forests
* sample size = 167,049
* features = ['drop off location id', 'pick up location id', 'trip miles', 'trip time','month','hour','weekday']
* target = 'total_passenger_fare'
* linear regression score: 0.81
* linear regression mean absolute error: $6.51
* linear regression mean squared error: $117.23
* random forests score: 0.85
* random forests mean absolute error: $5.25
* random forests mean squared error: $91.66

### Machine Learning Model 2. Linear Regression vs Neural Networks
* sample size = 
* features = ['drop off location id', 'pick up location id', 'trip miles', 'trip time', 'congestion_surcharge', 'tips', 'month','day','hour', 'minute']
* target = 'base_passenger_fare'
* linear regression score: 0.75
* linear regression mean absolute error: $6.39
* linear regression mean squared error: $119.83
* neural network trip mileage sensitivity analysis
* all distance trips
  * neural network mean absolute error: $3.51
  * neural network root mean squared error: $5.52
* trips less than 20 miles long
  * neural network mean absolute error: $3.29
  * neural network root mean squared error: $4.96

### Machine Learning Model 3. Linear Regression 
* sample size = 337,579
* features = 
* target = 'base_passenger_fare'
* linear regression score: 0.79
* linear regression mean absolute error: $5.52
* linear regression mean squared error: $113.67

## Conclusion
