# Import dependencies
import pandas as pd
# from json import loads, dumps
from flask import Flask, render_template_string #, send_file, Response
from flask_cors import CORS
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
df = pd.read_csv('Projects/test/NYC-Taxis/static/data/uber_nyc_2023_1.csv')
df_ints = df.drop(columns=['hvfhs_license_num', 'request_datetime', 'date', 'PUBorough', 'PUZone', 'DOBorough', 'DOZone'])

# Actual DFs to use
# df_1 = pd.read_csv('Projects/test/NYC-Taxis/static/data/uber_nyc_2023_1.csv')
# df_2 = pd.read_csv('Projects/test/NYC-Taxis/static/data/uber_nyc_2023_2.csv')
# df_3 = pd.read_csv('Projects/test/NYC-Taxis/static/data/uber_nyc_2023_3.csv')
# new_df = pd.concat([df_1, df_2, df_3])
# new_df_ints = new_df.drop(columns=['hvfhs_license_num', 'request_datetime', 'date', 'PUBorough', 'PUZone', 'DOBorough', 'DOZone'])



# Create heatmap with Seaborn
def create_heatmap():
    sns.set_style(style="darkgrid")
    fig, ax = plt.subplots()
    sns.heatmap(round(df_ints.corr(),2), annot=True, cmap='PuBuGn', ax=ax).set_title('Related Features')

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


# Helper function to create a Matplotlib plot
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

@app.route('/seaborn')
def seaborn_plot():
    plot_url = create_heatmap()
    html = f'<img src="data:image/png;base64,{plot_url}" alt="Seaborn Plot">'
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


if __name__ == '__main__':
    app.run(debug=True)
