# NYC-Taxis
Project 4

## Introduction

For this project, we analyzed Uber trips taken in NYC for all of 2023. This data was pulled from the official NYC database provided by the NYC Taxi and Limousine Commission (TLC), which contains trip records for nearly 15 years (https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page). In particular, we were interested in analyzing the Uber trips, located in the High Volume For-Hire Vehicle (FHV) Trip Data, pulled from NYC OpenData (https://data.cityofnewyork.us/Transportation/2023-High-Volume-FHV-Trip-Data/u253-aew4/about_data).

This dataset contains a row for each trip taken by FHV's in 2023. This includes Uber, Lyft, Via, and Juno. In effort to reduce the number of data points to observed, we limited to Uber data. This allowed us to get a focused dataset for one of the most popular forms of taxis in the city. The trip data is comprehensive, containing fields such as pickup and dropoff locations (based on the TLC Taxi Zone), base passenger fare, tips, trip time and miles, tax, and total driver pay to name a few.

We created 3 supervised machine learning models to find if the data would be able to predict the base passenger fare using various features. To this end, we utilized a frontend HTML and JavaScript, and connected the data from python via Flask API.

## Process

### 1. Extract, Transform, Load
Upon identifying the data as too large to analyze, we sought to reduce the dataset to a manageable, random sample. We utilized Databricks to read the parquet files for each month in 2023, and leveraged PySpark to .....


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

### Machine Learning Model 1. Linear Regression
sample size = 
features = ['trip_miles', 'trip_time', 'tolls', 'congestion_surcharge']
target = 'base_passenger_fare'
linear regression score: 0.79
linear regression mean absolute error: 
linear regression mean squared error: $113.83

### Machine Learning Model 2. Linear Regression vs Random Forests
sample size = 167,049
features = ['drop off location id', 'pick up location id', 'trip miles', 'trip time','month','hour','weekday']
target = 'total_passenger_fare'
linear regression score: 0.81
linear regression mean absolute error: $6.51
linear regression mean squared error: $117.23
random forests score: 0.85
random forests mean absolute error: #
random forests mean squared error: 

### Machine Learning Model 3. Linear Regression vs Neural Networks
sample size = 87,825
features = []
target = 'base_passenger_fare'
linear regression score: xx
linear regression mean absolute error: 
linear regression mean squared error: 
neural network trip mileage sensitivity analysis
all distance trips
neural network loss: 30.55
neural network mean absolute error: $3.53
neural network root mean squared error: $5.53
trips less than 20 miles long
neural network loss: 23.94
neural network mean absolute error: $3.24
neural network root mean squared error: $4.89

## Conclusion