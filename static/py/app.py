# Import dependencies
import pandas as pd
# from json import loads, dumps
from flask import Flask, render_template_string, jsonify #, send_file, Response
from flask_cors import CORS

# Set the backend to 'Agg
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
df = pd.read_csv('static/data/uber_nyc_2023_1.csv')
# df_ints = df.drop(columns=['Unnamed: 0', 'hvfhs_license_num', 'request_datetime', 'date', 'PUBorough', 'PUZone', 'DOBorough', 'DOZone'])

# Actual DFs to use
# df_1 = pd.read_csv('../data/uber_nyc_2023_1.csv')
# df_2 = pd.read_csv('../data/uber_nyc_2023_2.csv')
# df_3 = pd.read_csv('../data/uber_nyc_2023_3.csv')
# new_df = pd.concat([df_1, df_2, df_3])
# new_df_ints = new_df.drop(columns=['hvfhs_license_num', 'request_datetime', 'date', 'PUBorough', 'PUZone', 'DOBorough', 'DOZone'])



# TESTING
# def get_coords():
    # # Import coordinates DataFrame
    # coordinates_df = pd.read_csv('static/data/taxi_zone_lookup_coordinates.csv')


#     # Merge df with coordinates_df on DOLocationID
#     df_merged_DO = pd.merge(df, coordinates_df, left_on='DOLocationID', right_on='LocationID', suffixes=('', '_DO'))

#     # Merge the resulting dataframe with coordinates_df again on PULocationID
#     df_merged_both = pd.merge(df_merged_DO, coordinates_df, left_on='PULocationID', right_on='LocationID', suffixes=('_DO', '_PU'))

#     # Drop the additional 'LocationID' columns from the merges
#     df_merged_both = df_merged_both.drop(columns=['LocationID_DO', 'LocationID_PU', 'service_zone_DO', 'service_zone_PU', 
#                                                 'Borough_PU', 'Zone_PU','Borough_DO', 'Zone_DO'
#                                                 ])

#     # Bin the DOLocationID's into 10 columns based on frequency
#     DO_qc = pd.qcut(df_merged_both['DOLocationID'].value_counts(), q=10, precision=0)
#     df_bins_DO = pd.merge(df_merged_both, DO_qc, left_on='DOLocationID', right_index=True)
#     df_bins_DO = df_bins_DO.rename(columns={'count': 'DO_bins'})

#     # Bin the PULocationID's into 10 columns based on frequency
#     PU_qc = pd.qcut(df_merged_both['PULocationID'].value_counts(), q=10, precision=0)
#     df_coord_bins_final = pd.merge(df_bins_DO, PU_qc, left_on='PULocationID', right_index=True)
#     df_coord_bins_final = df_coord_bins_final.rename(columns={'count': 'PU_bins'})

#     df_coord_bins_final = df_coord_bins_final[['DOLocationID', 'PULocationID', 'DO_bins', 'PU_bins']]

#     df_coord_bins_final = df_coord_bins_final.astype({'DO_bins': 'object', 'PU_bins': 'object'})

#     return df_coord_bins_final.to_json(orient="records")



# Create heatmap with Seaborn
def create_heatmap():

    # Reduce to only int or float columns
    df_ints = df.drop(columns=['Unnamed: 0', 'hvfhs_license_num', 'request_datetime', 'date', 'PUBorough', 'PUZone', 'DOBorough', 'DOZone'])

    # Set the style of the plot
    sns.set_style(style="darkgrid")
    
    # Initialize subplot for this plot
    fig, ax = plt.subplots(figsize=(9,9))

    # Create the heatmap
    sns.heatmap(round(df_ints.corr(),2), annot=True, cmap='PuBuGn', ax=ax).set_title('Related Features')

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


# Helper function to create a Matplotlib plot (EXAMPLE DATA)
def create_matplotlib_plot():
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3, 4], [1, 4, 2, 3])
    ax.set(xlabel='x-axis', ylabel='y-axis', title='Matplotlib Plot')
    
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

# Endpoint for Matplotlib plot
@app.route('/matplotlib')
def matplotlib_plot():
    plot_url = create_matplotlib_plot()
    html = f'<img src="data:image/png;base64,{plot_url}" alt="Matplotlib Plot">'
    return render_template_string(html)


# # Set endpoint for JSON:
# @app.route('/coordinates.json')
# def get_coordinates(): 
#     return jsonify(get_coords())


if __name__ == '__main__':
    app.run(debug=True)
