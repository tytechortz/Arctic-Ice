import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import sqlite3
from dash.dependencies import Input, Output
import time
from datetime import datetime
from pandas import Series
from scipy import stats 
from numpy import arange,array,ones 
from scipy.stats import norm
from pandas import DatetimeIndex

app = dash.Dash(__name__)
app.config['suppress_callback_exceptions']=True

pd.options.display.float_format = '{:,}'.format

value_range = [0, 365]

# Read data
df = pd.read_csv('ftp://sidads.colorado.edu/DATASETS/NOAA/G02186/masie_4km_allyears_extent_sqkm.csv', skiprows=1)


# Format date and set indext to date
df['yyyyddd'] = pd.to_datetime(df['yyyyddd'], format='%Y%j')
df.set_index('yyyyddd', inplace=True)
df.columns = ['Total Arctic Sea', 'Beaufort Sea', 'Chukchi Sea', 'East Siberian Sea', 'Laptev Sea', 'Kara Sea',\
     'Barents Sea', 'Greenland Sea', 'Bafin Bay Gulf of St. Lawrence', 'Canadian Archipelago', 'Hudson Bay', 'Central Arctic',\
         'Bering Sea', 'Baltic Sea', 'Sea of Okhotsk', 'Yellow Sea', 'Cook Inlet']

df1 = df['Total Arctic Sea']

count_row = df.shape[0]
days = count_row

# Dropdown year selector values
year_options = []
for YEAR in df.index.year.unique():
    year_options.append({'label':(YEAR), 'value':YEAR})

# Dropdown month selector values
month_options = [
{'label':'JAN', 'value':1},
{'label':'FEB', 'value':2},
{'label':'MAR', 'value':3},
{'label':'APR', 'value':4},
{'label':'MAY', 'value':5},
{'label':'JUN', 'value':6},
{'label':'JUL', 'value':7},
{'label':'AUG', 'value':8},
{'label':'SEP', 'value':9},
{'label':'OCT', 'value':10},
{'label':'NOV', 'value':11},
{'label':'DEC', 'value':12}
]

# Dropdown sea selector values
sea_options = []
for sea in df.columns.unique():
    sea_options.append({'label':sea, 'value':sea})

# Change dataframe to 5 day trailing average
df_fdta = df.rolling(window=5).mean()
# print(df_fdta['Total Arctic Sea'].iloc[-2])

startyr = 2006
presentyr = datetime.now().year
last_year = presentyr-1
year_count = presentyr-startyr
presentday = datetime.now().day
dayofyear = time.strftime("%j")
dayofyear = int(dayofyear)

arctic = df['Total Arctic Sea']
years = []


year_dict = {}
keys = []


for i in df.index.year.unique():
    keys.append(i)

def dictionary_maker():
    for i in keys:
        year_dict[i] = 0
keys = [str(i) for i in keys]
dictionary_maker()



m = 1
d = 1

arctic_r = arctic[(arctic.index.month == m) & (arctic.index.day == d)]
sort_arctic_r = arctic_r.sort_values(axis=0, ascending=True)

def get_layout():
    return html.Div(
        [
            html.Div([
                html.H2(
                    'Arctic Sea Ice Extent',
                    className='twelve columns',
                    style={'text-align': 'center'}
                ),
            ],
                className='row'
            ),
            html.Div([
                html.H6(
                    '2006-Present',
                    className='twelve columns',
                    style={'text-align': 'center'}
                ),
            ],
                className='row'
            ),
            html.Div([
                html.H6(
                    'Data From National Snow and Ice Data Center',
                    className='twelve columns',
                    style={'text-align': 'center'}
                ),
            ],
                className='row'
            ),
            html.Div([
                html.Div([
                    html.Label('Select Product'),
                    dcc.RadioItems(
                        id='product',
                        options=[
                            {'label':'Ice Exent By Year', 'value':'years-graph'},
                            {'label':'Avg Monthy Extent', 'value':'monthly-bar'},
                        ],
                        # value='temp-graph',
                        labelStyle={'display': 'block'},
                    ),
                ],
                    className='three columns',
                ),
                html.Div([
                    html.Div(id='sea-selector'),
                ],
                    className='two columns'
                ),
                html.Div([
                    html.Div(id='month-selector'),
                ],
                    className='two columns'
                ),
            ],
                className='row'
            ),
            html.Div([
                html.Div([
                    html.Div(
                        id='graph'
                    ),
                ],
                    className='eight columns'
                ),
                html.Div([
                    html.Div([
                        html.Div(id='year-selector'),
                    ],
                        className='four columns'
                    ),
                    html.Div([
                        html.Div(id='bar-stats'
                        ),
                    ],
                        className='twelve columns'
                    ),
                ],
                    className='four columns'
                ),
            ],
                className='row'
            ),
            html.Div(id='df-monthly', style={'display': 'none'}),
    ])

app.layout = get_layout

@app.callback(
    Output('bar-stats', 'children'),
    [Input('df-monthly', 'children'),
    Input('product','value')])
def display_graph_stats(ice, selected_product):
    df_monthly = pd.read_json(ice)
    # print(df_monthly)
    # df_monthly = df.apply(lambda x: pd.Series(x['data']),axis=1).stack().reset_index(level=1, drop=False)
    # df_monthly.columns = ['Extent', 'Anom']
    extent = df_monthly['data'].apply(pd.Series)
    extent['value'] = extent['value'].astype(float)
    extent = extent.sort_values('value')
    extent = extent[extent.value != -9999]
    print(extent)
    print(extent.iloc[0,0])

    if selected_product == 'monthly-bar':
        return html.Div([
                html.Div('10 Lowest Extents for January', style={'text-align': 'center'}),
                html.Div([
                    html.Div([
                        html.Div([
                            # create_value_rows()
                            html.Div('{}'.format(extent.iloc[i,0], style={'text-align': 'center'})) for i in range(10)
                            # html.Div('{}'.format(extent.iloc[1,0]), style={'text-align': 'center'}),
                        ],
                            className='six columns'
                        ),
                        html.Div([
                            # create_year_rows()
                            html.Div('{}'.format(extent.index[i], style={'text-align': 'center'})) for i in range(10)
                        ],
                            className='six columns'
                        ),
                    ],
                        className='row'
                    ),
                ],
                    className='round1'
                ),
                    
            ],
                className='round1'
            ),

@app.callback(
    Output('year-selector', 'children'),
    [Input('product', 'value')])
def display_year_selector(product_value):
    if product_value == 'years-graph':
        return html.P('Select Years') ,dcc.Checklist(
            id='selected-years',
            options=year_options,       
                )

@app.callback(
    Output('sea-selector', 'children'),
    [Input('product', 'value')])
def display_sea_selector(product_value):
    if product_value == 'years-graph':
        return html.P('Select Sea') ,dcc.Dropdown(
            id='selected-sea',
            options=sea_options,      
                )

@app.callback(
    Output('month-selector', 'children'),
    [Input('product', 'value')])
def display_month_selector(product_value):
    if product_value == 'monthly-bar':
        return html.P('Select Month') ,dcc.Dropdown(
            id='month',
            options=month_options,
            value=1     
                )

@app.callback(
    Output('graph', 'children'),
    [Input('product', 'value')])
def display_graph(value):
    if value == 'years-graph':
        return dcc.Graph(id='ice-extent')
    elif value == 'monthly-bar':
        return dcc.Graph(id='monthly-bar')

@app.callback(
    Output('ice-extent', 'figure'),
    [Input('selected-sea', 'value'),
    Input('selected-years', 'value')])
def update_figure(selected_sea, selected_year):
    # print(selected_year)
    traces = []
    # selected_years = [selected_year1,selected_year2,selected_year3,selected_year4]
    for year in selected_year:
        sorted_daily_values=df_fdta[df_fdta.index.year == year]
        traces.append(go.Scatter(
            y=sorted_daily_values[selected_sea],
            mode='lines',
            name=year
        ))
    return {
        'data': traces,
        'layout': go.Layout(
                title = '{} Ice Extent'.format(selected_sea),
                xaxis = {'title': 'Day', 'range': value_range},
                yaxis = {'title': 'Ice extent (km2)'},
                hovermode='closest',
                )  
    }

@app.callback([
    Output('monthly-bar', 'figure'),
    Output('df-monthly', 'children')],
    [Input('month', 'value')])
def update_figure_b(month_value):
    df_monthly = pd.read_json('https://www.ncdc.noaa.gov/snow-and-ice/extent/sea-ice/N/' + str(month_value) + '.json')
    df_monthly = df_monthly.iloc[5:]
    ice = []
    for i in range(len(df_monthly['data'])):
        ice.append(df_monthly['data'][i]['value'])
    ice = [14.42 if x == -9999 else x for x in ice]
    ice = list(map(float, ice))
    
    
    # trend line
    def fit():
        xi = arange(0,len(ice))
        slope, intercept, r_value, p_value, std_err = stats.linregress(xi,ice)
        return (slope*xi+intercept)

    data = [
        go.Bar(
            x=df_monthly['data'].index,
            y=ice
        ),
        go.Scatter(
                x=df_monthly['data'].index,
                y=fit(),
                name='trend',
                line = {'color':'red'}
            ),

    ]
    layout = go.Layout(
        xaxis={'title': 'Year'},
        yaxis={'title': 'Ice Extent-Million km2', 'range':[(min(ice)-1),(max(ice)+1)]},
        title='{} Avg Ice Extent'.format(month_options[int(month_value)- 1]['label']),
        plot_bgcolor = 'lightgray',
    )
    return {'data': data, 'layout': layout}, df_monthly.to_json()

# @app.callback(
#     Output('graph', 'children'),
#     [Input('year', 'value')])
# def display_graph(value):
#     print(value)
#     if value == False:
#         return html.Div([
#             html.Div([
#                 dcc.Graph(id='ice'),
#             ]),
            # html.Div([
            #     dcc.Slider(
            #         id='rev-map-year',
            #             min = 2014,
            #             max = 2018,
            #             marks={i: '{}'.format(i) for i in range(2014,2019)}, 
            #             step = 1,
            #             value = 2014,
            #             # vertical = False,
            #             updatemode = 'drag'
            #         )   
            # ])
        # ]) 


if __name__ == "__main__":
    app.run_server(port=8050, debug=False)
