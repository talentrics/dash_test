import pandas as pd
from threading import Thread
import json
import requests
import datetime
import jinja2

from bokeh.embed import server_document, components 
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, HoverTool, TextInput, CustomJS
from bokeh.io import curdoc
from bokeh.plotting import figure, output_file, show, curdoc
from bokeh.server.server import Server
from bokeh.themes import Theme
from bokeh.resources import CDN
from bokeh.embed import file_html

API_URL = "https://www.alphavantage.co/query" 
data = { "function": "TIME_SERIES_DAILY_ADJUSTED",
        "symbol":'AAPL',
        "outputsize" : "full",
        "datatype": "json",
        "apikey": "VWSYI59PA94WNUMQ" }
response = requests.get(API_URL, data)
response_json = response.json()

df = pd.DataFrame.from_dict(response_json['Time Series (Daily)'], orient= 'index').sort_index(axis=1)
df = df.rename(columns={ '1. open': 'Open', '2. high': 'High', '3. low': 'Low', '4. close': 'Close', '5. adjusted close': 'Adj Close', '6. volume': 'Volume', '7. dividend amount': 'Dividend Amount', '8. split coefficient': 'Split Coefficient'})
df.reset_index(inplace=True)
df['index'] = pd.to_datetime(df['index'])
mask = (df['index'] >= '2020-01-01')
df = df.loc[mask]
df1 = df[[ 'index', 'Open', 'Close', 'Adj Close']]

p = figure(plot_width=800 ,plot_height=800, x_axis_type="datetime")
p.background_fill_color="#f5f5f5"
p.grid.grid_line_color="white"
p.title.text = 'Monthly Stock Data of %s % APPL.upper'
p.xaxis.axis_label = "Date and Month of 2020"
p.yaxis.axis_label = "Price"
p.axis.axis_line_color = None
p.title.text_font = "Times"
p.title.text_font_size = "20px"

components(p)