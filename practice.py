import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import sqlite3
from dash.dependencies import Input, Output
import datetime as dt 

# from app import app

# database connection
cnx = sqlite3.connect('sea-ice.db')

# Launch the application:
app = dash.Dash(__name__)

# Create a DataFrame from the .csv file:
# df = pd.read_sql_query("SELECT * FROM ice", cnx)
#  df = pd.read_csv('./sea_ice.csv')
df2 = pd.read_csv('ftp://sidads.colorado.edu/DATASETS/NOAA/G02186/masie_4km_allyears_extent_sqkm.csv', skiprows=1)

# df2.columns = range(df2.shape[1])
df2[0] = pd.to_datetime(df2['yyyyddd'], format='%Y%j')
print(df2.head())





value_range = [0, 365]

app.layout = html.Div([
    html.Div(
        className="app-header",
        children=[
            html.Div('Arctic Sea Ice Extent', className="app-header--title"),
        ]
    ),
    html.Div(
        children=html.Div(
             html.H3(children='1988-Present')
        )
    ),
    dcc.Graph(
        id='ice-extent'),
        html.Div([
            dcc.RangeSlider(
                id='ice-slider',
                min=value_range[0],
                max=value_range[1],
                step=1,
                value=[0, 365],
                # marks={i: i for i in range(value_range[0], value_range[1]+ 1)}
            ),
            html.Div([
            html.H2('Slider to Select Day Range')
        ]),
        ]),
        html.Div([
            html.H2('Select Years'),
        ]),
        html.Div([
            html.Div([
                dcc.Dropdown(
                id='year1',
                options=[{'label': i, 'value': i} for i in years],
                placeholder='select years',
                value="2012"),
            ],
            style={'width': '25%', 'display': 'inline-block'}),
            html.Div([
                dcc.Dropdown(
                id='year2',
                options=[{'label': i, 'value': i} for i in years],
                placeholder='select years',
                value="2016"),
            ],
            style={'width': '25%', 'display': 'inline-block'}),
            html.Div([
                dcc.Dropdown(
                id='year3',
                options=[{'label': i, 'value': i} for i in years],
                placeholder='select years',
                value="2018"),
            ],
            style={'width': '25%', 'display': 'inline-block'}),
            html.Div([
                dcc.Dropdown(
                id='year4',
                options=[{'label': i, 'value': i} for i in years],
                placeholder='select years',
                value="2019"),
            ],
            style={'width': '25%', 'float': 'right', 'display': 'inline-block'}),        
            ]),

        html.Div([
            html.H2('Select Decade Average'),
        ]),

        dcc.RadioItems(
            id='decade-avg',
            options=[
                {'label': "1980's Average", 'value': "1980's Average"},
                {'label': "1990's Average", 'value': "1990's Average"},
                {'label': "2000's Average", 'value': "2000's Average"},
                {'label': "2010's Average", 'value': "2010's Average"}
            ],
            value="1980's Average",
            # labelStyle={'display': 'inline-block'},
            style={'margin': '0 auto', 'text-align': 'center'}
        )
])

@app.callback(
    Output('ice-extent', 'figure'),
    [Input('year1', 'value'),
    Input('year2', 'value'),
    Input('year3', 'value'),
    Input('year4', 'value'),
    Input('ice-slider', 'value'),
    Input('decade-avg', 'value')])
def update_graph(selected_year1, selected_year2, selected_year3, selected_year4, value_range, decade):
    traces = []
    traces.append(go.Scatter(
            x=df['#num'],
            y=df[selected_year1],
            mode='lines',
            name=selected_year1
        ))
    traces.append(go.Scatter(
            x=df['#num'],
            y=df[selected_year2],
            mode='lines',
            name=selected_year2
        ))
    traces.append(go.Scatter(
            x=df['#num'],
            y=df[selected_year3],
            mode='lines',
            name=selected_year3
        ))
    traces.append(go.Scatter(
            x=df['#num'],
            y=df[selected_year4],
            mode='lines',
            name=selected_year4
        ))
    traces.append(go.Scatter(
            x=df['#num'],
            y=df[decade],
            mode='lines',
            name=decade
    ))
    traces.append(go.Scatter(
            x=df['#num'],
            y=df2[1],
            mode='lines',
            
    ))
    return {
        'data': traces,
        'layout': go.Layout(
                height = 800,
                title = 'Arctic Sea Ice Extent',
                xaxis = {'range': value_range, 'title': 'Day'},
                yaxis = {'title': 'Ice extent (km2)'},
                hovermode='closest',
                )  
    }


    
# Add the server clause:
if __name__ == '__main__':
    app.run_server()