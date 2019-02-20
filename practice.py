import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import pandas as pd
import sqlite3
from dash.dependencies import Input, Output
import time
# import datetime
from datetime import datetime
from pandas import Series
from scipy import stats 
from numpy import arange,array,ones 



app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config['suppress_callback_exceptions']=True

pd.options.display.float_format = '{:,}'.format

df = pd.read_csv('ftp://sidads.colorado.edu/DATASETS/NOAA/G02186/masie_4km_allyears_extent_sqkm.csv', skiprows=1)

df['yyyyddd'] = pd.to_datetime(df['yyyyddd'], format='%Y%j')

value_range = [0, 365]

year_options = []
for YEAR in df['yyyyddd'].dt.strftime('%Y').unique():
    year_options.append({'label':(YEAR), 'value':YEAR})

# df2=df[(df['yyyyddd'].dt.year == 2017)]


today_value = df[' (0) Northern_Hemisphere'].iloc[-1]
daily_difference = df[' (0) Northern_Hemisphere'].iloc[-1] - df[' (0) Northern_Hemisphere'].iloc[-2]
record_low = df[' (0) Northern_Hemisphere'].min(),
df[' (0) Northern_Hemisphere'].iloc[-1]
record_low_difference = today_value - record_low[0]

df2=pd.read_csv('ftp://sidads.colorado.edu/DATASETS/NOAA/G02186/masie_4km_allyears_extent_sqkm.csv', skiprows=1)
df2['yyyyddd'] = pd.to_datetime(df2['yyyyddd'], format='%Y%j')
df2.set_index('yyyyddd', inplace=True)
df3 = df2[' (0) Northern_Hemisphere'].loc[df2.groupby(pd.Grouper(freq='Y')).idxmax().iloc[:-1, 0]]
df3.sort_values(axis=0, ascending=False)


annual_maximums = df2[' (0) Northern_Hemisphere'].loc[df2.groupby(pd.Grouper(freq='Y')).idxmax().iloc[:-1, 0]]


body = html.Div([
    dbc.Row([
        dbc.Col(
            html.Div(
                className="app-header",
                children=[
                    html.Div('Arctic Sea Ice Extent', className="app-header--title"),
                ]
            ),
        )
    ]),
    dbc.Row([
        dbc.Col(
            html.H3('1988-Present'),
        ),
    ]),
    dbc.Row([
        dbc.Col(
            html.H3('Data From National Snow and Ice Data Center'),
        ),
    ]),
    dbc.Row(
        [
            dbc.Col(
                html.Div([
                    dcc.Graph(id='ice-extent', style={'height':700}),    
                ]),
                width={'size':10}
            ),
        ],
        justify='around'
    ),
    dbc.Row([
        dbc.Col(
            html.H2('Select Years'),
        ),
    ]),
    dbc.Row(
        [
            dbc.Col(
                dcc.Dropdown(id='year1',options=year_options,value="2007"
                ),
                width={'size':2, 'offset': 5}),
        ],
    ),
]),

# app.layout = html.Div([
#     html.Div(
#         className="app-header",
#         children=[
#             html.Div('Arctic Sea Ice Extent', className="app-header--title"),
#         ]
#     ),
#     html.Div(
#         children=html.Div(
#              html.H3(children='1988-Present'),
#         )
#     ),
#     html.Div(
#         children=html.Div(
#              html.H3(children='Data From National Snow and Ice Data Center'),
#         )
#     ),
#     dcc.Graph(
#         id='ice-extent'),
#         html.Div([
#             dcc.RangeSlider(
#                 id='ice-slider',
#                 min=value_range[0],
#                 max=value_range[1],
#                 step=1,
#                 value=[0, 365],
#                 # marks={i: i for i in range(value_range[0], value_range[1]+ 1)}
#             ),
#             html.Div([
#             html.H2('Slider to Select Day Range')
#         ]),
#         ]),
#         html.Div([
#             html.H2('Select Years'),
#         ]),
#         html.Div([
#             html.Div([
#                 dcc.Dropdown(
#                 id='year1',
#                 options=year_options,
#                 value="2007"),
#             ],
#             style={'width': '20%', 'display': 'inline-block'}),
#             html.Div([
#                 dcc.Dropdown(
#                 id='year2',
#                 options=year_options,
#                 value="2012"),
#             ],
#             style={'width': '20%', 'display': 'inline-block'}),
#             html.Div([
#                 dcc.Dropdown(
#                 id='year3',
#                 options=year_options,
#                 value="2016"),
#             ],
#             style={'width': '20%', 'display': 'inline-block'}),
#             html.Div([
#                 dcc.Dropdown(
#                 id='year4',
#                 options=year_options,
#                 value="2018"),
#             ],
#             style={'width': '20%', 'float': 'right', 'display': 'inline-block'}),
#             html.Div([
#                 dcc.Dropdown(
#                 id='year5',
#                 options=year_options,

#                 value="2019"),
#             ],
#             style={'width': '20%', 'float': 'right', 'display': 'inline-block'}),       
#             ]),

#     html.Div([
#             html.H2("Today's Value: {:,.1f} km2".format(today_value)),
#         ]),

#      html.Div([
#             html.H2("24 Hour Change: {:,.1f} km2".format(daily_difference)),
#         ]),   

#     html.Div([
#             html.H2('Record Minimum: {:,.1f} km2'.format(record_low[0])),
#         ]),
#     html.Div([
#             html.H2('Difference From Minimum: {:,.1f} km2'.format(record_low_difference)),
#         ]),

#     html.Div([

#     ])
      


html.Ul([html.Li(x) for x in annual_maximums.sort_values(ascending=True)]) 

@app.callback(
    Output('ice-extent', 'figure'),
    [Input('year1', 'value')])
def update_figure(selected_year1):
    traces = []
    selected_years = [selected_year1]
    for year in selected_years:
        df2=df[(df['yyyyddd'].dt.year == int(year))]
        traces.append(go.Scatter(
            # x=df2['yyyyddd'],
            y=df2[' (0) Northern_Hemisphere'],
            mode='lines',
            name=year
        ))
    return {
        'data': traces,
        'layout': go.Layout(
                title = 'Arctic Sea Ice Extent',
                xaxis = {'title': 'Day', 'range': value_range},
                yaxis = {'title': 'Ice extent (km2)'},
                hovermode='closest',
                )  
    }

app.layout = html.Div(body)

if __name__ == "__main__":
    app.run_server(port=8124, debug=True)