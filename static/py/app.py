# Import dependencies
import pandas as pd
# from json import loads, dumps
from flask import Flask, render_template_string, jsonify #, send_file, Response
from flask_cors import CORS

# Set the backend to 'Agg'
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
# from matplotlib.figure import Figure
# from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import seaborn as sns
from io import BytesIO #, StringIO
import numpy as np
import base64

# Older df, used for testing
df = pd.read_csv('NYC-Taxis/static/data/uber_nyc_2023_1.csv')
# Select numeric columns from the DataFrame
numeric_df = df.select_dtypes(include=[float, int]).drop(columns=['Unnamed: 0'])

# Select features for cluster data
features = ['trip_miles', 'trip_time', 'base_passenger_fare', 'tolls', 'sales_tax', 'congestion_surcharge', 'airport_fee', 'tips']
data = df[features].dropna()



# Actual DFs to use
# df_1 = pd.read_csv('../data/uber_nyc_2023_1.csv')
# df_2 = pd.read_csv('../data/uber_nyc_2023_2.csv')
# df_3 = pd.read_csv('../data/uber_nyc_2023_3.csv')
# df = pd.concat([df_1, df_2, df_3])

# FUNCTIONS FOR VISUALIZATIONS

# Get the coordinates of taxi zones
def get_coords():
    # Import coordinates df
    df_taxi_zones = pd.read_csv('NYC-Taxis/static/data/taxi_zone_lookup_coordinates.csv')

    # Merge df with coordinates_df on DOLocationID
    df_merged_DO = pd.merge(df, df_taxi_zones, left_on='DOLocationID', right_on='LocationID', suffixes=('', '_DO'))

    # Merge the resulting dataframe with coordinates_df again on PULocationID
    df_merged_both = pd.merge(df_merged_DO, df_taxi_zones, left_on='PULocationID',\
                              right_on='LocationID', suffixes=('_DO', '_PU'))\
                            .drop(columns=['LocationID_DO', 'LocationID_PU', 'service_zone_DO',\
                                           'service_zone_PU', 'Borough_PU', 'Zone_PU','Borough_DO', 'Zone_DO'])
    
    return df_merged_both


# Get the zones for dropoff or pickup, binned by frequency
def get_zones(df, col):
    # Reduce the columns
    df = df[['DOLocationID', 'PULocationID']]

    # Set variable for the column not being called - used for dropping
    for i in df.columns:
        if col != i:
            other_col = i

    # Set 5 bins based on frequency
    df[col[:2] + "_bins"] = pd.cut(df[col], bins = 5, precision = 0,  labels=['Infrequent', 'Frequent',\
                                                                             'Regular', 'Common', 'Very Common'])

    # Reduce to unique taxi zone ID's
    df = df.drop_duplicates(subset=[col]).drop(columns=[other_col])

    # Return JSON
    return df.to_json(orient='records')


# Create heatmap with Seaborn
def create_heatmap():

    # Set the style of the plot
    sns.set_style(style="darkgrid")
    
    # Initialize subplot for this plot
    fig, ax = plt.subplots(figsize=(9,9))

    # Create the heatmap
    sns.heatmap(round(numeric_df.corr(),2), annot=True, cmap='PuBuGn', ax=ax).set_title('Related Features')

    # Add a buffer in the memory before saving the figure and then returning a base64-encoded string
    buf = BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode('utf-8')


# Create histogram with Seaborn
def create_histogram():
    sns.set_style(style="darkgrid")
    fig, ax = plt.subplots()
    sns.histplot(np.log(df['base_passenger_fare'])+1, kde=True, ax=ax).set_title("Fares")
    
    buf = BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode('utf-8')


# Create boxplot for numeric columns
def create_boxplot():

    # Set the style of the plot
    sns.set_style(style="darkgrid")
    
    # Initialize subplot for this plot
    fig, ax = plt.subplots(figsize=(12, 8))

    # Create the boxplot
    sns.boxplot(data=numeric_df, palette="Set3", ax=ax)
    
    # Customize the plot
    ax.set_xticks(range(len(numeric_df.columns)))
    ax.set_xticklabels(numeric_df.columns, rotation=45)
    ax.set_title('Boxplot of Numeric Columns')
    ax.set_xlabel('Columns')
    ax.set_ylabel('Values')

    # Add a buffer in memory before saving the figure and then returning a base64-encoded string
    buf = BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode('utf-8')

# Create histplot for trip time
def create_trip_time_histplot():
    # Set the style of the plot
    sns.set_style(style="darkgrid")
    
    # Initialize subplot for this plot
    fig, ax = plt.subplots(figsize=(12, 8))

    # Create the histplot for 'trip_time' converted to minutes
    sns.histplot(data=numeric_df[['trip_time']].apply(lambda x: x / 60), kde=True, bins=60, ax=ax)
    
    # Customize the plot
    ax.set_title('Histogram of Trip Time')
    ax.set_xlabel('Trip Time (Minutes)')
    ax.set_ylabel('Values')

    # Add a buffer in memory before saving the figure and then returning a base64-encoded string
    buf = BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode('utf-8')

# Create histplot for tips
def create_tips_histplot():
    # Set the style of the plot
    sns.set_style(style="darkgrid")
    
    # Initialize subplot for this plot
    fig, ax = plt.subplots(figsize=(12, 8))

    # Create the histplot for 'tips' where tips are greater than 0
    sns.histplot(numeric_df[numeric_df["tips"] > 0]["tips"], color="blue", kde=True, label=None, bins=60, ax=ax)
    
    # Customize the plot
    ax.set_title('Histogram of Tips')
    ax.set_xlabel('Tips')
    ax.set_ylabel('Count')
    ax.grid(True)

    # Add a buffer in memory before saving the figure and then returning a base64-encoded string
    buf = BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode('utf-8')

# Create the pairplot for trip time, trip miles, and base passenger fare
def create_pairplot():
    # Set the style of the plot
    sns.set_style(style="darkgrid")
    
    # Create the pairplot for trip time, trip miles, and base passenger fare
    pairplot = sns.pairplot(numeric_df[['trip_time', 'trip_miles', 'base_passenger_fare']])

    # Customize the plot
    pairplot.figure.suptitle('Pairplot of Trip Time, Trip Miles, and Base Passenger Fare', y=1.02)

    # Add a buffer in memory before saving the figure and then returning a base64-encoded string
    buf = BytesIO()
    pairplot.savefig(buf, format='png')
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode('utf-8')


# Random Forests Matplotlib plot
def create_rf_importance_plot():
    df_rf_feature_importance = pd.read_csv('NYC-Taxis/static/data/rf_features.csv')
    df_rf_predictions = pd.read_csv('NYC-Taxis/static/data/rf_predictions.csv').iloc[0:50,:]
    fig, (ax1,ax2) = plt.subplots(2,figsize=(20,10))
    ax1.bar(df_rf_feature_importance['Feature'], df_rf_feature_importance['Importance (%)'].astype('float'))
    ax1.set(xlabel='Features', ylabel='Importance (%)', title='Feature Selection')#, fontsize='large')#, fontweight='bold')
    ax2.scatter(df_rf_predictions.index,df_rf_predictions['True Predictions'],marker='s')
    ax2.scatter(df_rf_predictions.index,df_rf_predictions['Random Forest Predictions Feature Selection'],marker='o')
    ax2.scatter(df_rf_predictions.index,df_rf_predictions['Linear Regression Predictions'],marker='D')
    ax2.set(xlabel='Testing Samples', ylabel='Predictions ($)', title='Regressor predictions n=20')
    ax2.legend(['True Predictions', 'Random Forest Predictions Feature Selection','Linear Regression Predictions'], fontsize="15", loc ="upper left")

    buf = BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode('utf-8')


# Establish Flask connection
app = Flask(__name__)
CORS(app)

@app.route('/heatmap')
def seaborn_plot():
    plot_url = create_heatmap()
    html = f'<img src="data:image/png;base64,{plot_url}" alt="Heatmap">'
    return render_template_string(html)

@app.route('/histogram')
def histogram():
    plot_url = create_histogram()
    html = f'<img src="data:image/png;base64,{plot_url}" alt="Histogram">'
    return render_template_string(html)

# Endpoint for Matplotlib boxplot
@app.route('/boxplot')
def matplotlib_plot():
    plot_url = create_boxplot()
    html = f'<img src="data:image/png;base64,{plot_url}" alt="Matplotlib Plot">'
    return render_template_string(html)

# Endpoint for histogram of trip time
@app.route('/trip_time_histplot')
def time_histplot():
    plot_url = create_trip_time_histplot()
    html = f'<img src="data:image/png;base64,{plot_url}" alt="Histogram Plot">'
    return render_template_string(html)

# Endpoint for histogram of tips
@app.route('/tips_histplot')
def tips_histplot():
    plot_url = create_tips_histplot()
    html = f'<img src="data:image/png;base64,{plot_url}" alt="Histogram Plot">'
    return render_template_string(html)

# Endpoint for pairplot
@app.route('/pairplot')
def pairplot():
    plot_url = create_pairplot()
    html = f'<img src="data:image/png;base64,{plot_url}" alt="Pairplot">'
    return render_template_string(html)

# Endpoint for Matplotlib plot random forests
@app.route('/rf_importance')
def rf_importance_plot():
    plot_url = create_rf_importance_plot()
    html = f'<img src="data:image/png;base64,{plot_url}" alt="Matplotlib Plot Random Forests Feature Importance">'
    return render_template_string(html)

# Set endpoint for JSON of dropoff zone frequencies
@app.route('/dropoff_zones.json')
def get_dropoffs(): 
    return jsonify(get_zones(df, 'DOLocationID'))

# Set endpoint for JSON of pickup zone frequencies
@app.route('/pickup_zones.json')
def get_pickups(): 
    return jsonify(get_zones(df, 'PULocationID'))


if __name__ == '__main__':
    app.run(debug=True)
