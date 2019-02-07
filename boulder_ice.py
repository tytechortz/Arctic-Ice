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
        dcc.Graph(id='ice-extent'),
    html.Div([
        dcc.Dropdown(id='year1',options=year_options,value=2019)
    ],
    style={'width': '48%', 'display': 'inline-block'}),

    ])
]) 

@app.callback(
    Output('ice-extent', 'figure'),
    [Input('year1', 'value')])
def update_figure(selected_year1):
    traces = []
    int(selected_year1)
    # print(type(selected_year1))
    df2=df[(df['yyyyddd'].dt.year == int(selected_year1))]
    traces.append(go.Scatter(
            x=df2.index,
            y=df2[' (0) Northern_Hemisphere'],
            mode='lines',
            name=selected_year1
        ))
    return {
        'data': traces,
        'layout': go.Layout(
                height = 800,
                title = 'Arctic Sea Ice Extent',
                xaxis = {'title': 'Day'},
                yaxis = {'title': 'Ice extent (km2)'},
                hovermode='closest',
                )  
    }

if __name__ == '__main__':
    app.run_server()   