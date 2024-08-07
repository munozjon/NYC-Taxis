# Import dependencies
import pandas as pd
from json import loads, dumps
from flask import Flask, render_template, send_file
from flask_cors import CORS
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import seaborn as sns
from io import StringIO, BytesIO

df = pd.read_csv('Projects/NYC-Taxis/static/data/jan_2023.csv')
df_ints = df.drop(columns=['hvfhs_license_num', 'request_datetime', 'PUBorough', 'PUZone', 'DOBorough', 'DOZone'])
fig, ax =  plt.subplots(figsize=(10,10))
ax = sns.set_style(style='darkgrid')

# Establish Flask connection
app = Flask(__name__)
CORS(app)


@app.route('/heatmap')
def heatmap():
    plt.cla()
    plt.clf()
    sns.heatmap(round(df_ints.corr(),2), annot=True, cmap='PuBuGn').set_title('Related Features')
    canvas = FigureCanvas(fig)
    img = BytesIO()
    fig.savefig(img)
    img.seek(0)
    return send_file(img, mimetype='png')



if __name__ == '__main__':
    app.run(debug=True)
