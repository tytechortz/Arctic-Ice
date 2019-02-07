import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import sqlite3
from dash.dependencies import Input, Output
import datetime as dt 

app = dash.Dash(__name__)

df = pd.read_csv('ftp://sidads.colorado.edu/DATASETS/NOAA/G02186/masie_4km_allyears_extent_sqkm.csv', skiprows=1)

df['yyyyddd'] = pd.to_datetime(df['yyyyddd'], format='%Y%j')



year_options = []
for YEAR in df['yyyyddd'].dt.strftime('%Y').unique():
    year_options.append({'label':(YEAR), 'value':YEAR})


app.layout = html.Div([
    html.Div([
        html.H1('Arctic Sea Ice Extent in km2', style={'align': 'center', 'color': 'blue'}),
        html.H3('Data from:', style={'align': 'center', 'color': 'blue'}),
        dcc.Graph(id='graph'),
            html.Div([
                dcc.Dropdown(id='year-picker1',options=year_options,value=df['yyyyddd'].min()),
            ],
            style={'width': '48%', 'display': 'inline-block'}),

    ])
])    

if __name__ == '__main__':
    app.run_server()   