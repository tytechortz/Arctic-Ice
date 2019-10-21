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
# df_fdta = df.rolling(window=5).mean()
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
                            {'label':'Extent Stats', 'value':'extent-stats'},
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
                        className='three columns'
                    ),
                    html.Div([
                        html.Div(id='current-stats'
                        ),
                    ],
                        className='nine columns'
                    ),
                    html.Div([
                        html.Div(id='bar-stats'
                        ),
                    ],
                        className='twelve columns'
                    ),
                    html.Div([
                        html.Div(
                            id='daily-rankings'
                        ),
                    ],
                        className='seven columns'   
                    ),
                    html.Div([
                        html.Div(
                            id='annual-rankings'
                        ),
                    ],
                        className='four columns'   
                    ),
                ],
                    className='four columns'
                ),
            ],
                className='row'
            ),
            html.Div(id='df-monthly', style={'display': 'none'}),
            html.Div(id='df-fdta', style={'display': 'none'}),
    ])

app.layout = get_layout



@app.callback(
    Output('daily-rankings-graph', 'figure'),
    [Input('product', 'value'),
    Input('selected-sea', 'value'),
    Input('df-fdta', 'children')])
def update_figure_b(selected_product, selected_sea, df_fdta):
    df_fdta = pd.read_json(df_fdta)
    print(selected_product)
    dr = df_fdta[(df_fdta.index.month == df_fdta.index[-1].month) & (df_fdta.index.day == df_fdta.index[-1].day)]
    dr_sea = dr[selected_sea]
    dr_sea.index = dr_sea.index.strftime('%Y-%m-%d')
    
    # trend line
    def fit():
        xi = arange(0,len(dr_sea))
        slope, intercept, r_value, p_value, std_err = stats.linregress(xi,dr_sea)
        return (slope*xi+intercept)

    data = [
        go.Bar(
            x=dr_sea.index,
            y=dr_sea,
            name=('Extent')
        ),
        go.Scatter(
                x=dr_sea.index,
                y=fit(),
                name='trend',
                line = {'color':'red'}
            ),

    ]
    layout = go.Layout(
        xaxis={'title': 'Year'},
        yaxis={'title': 'Ice Extent-Million km2'},
        title='{} Values on {}'.format(selected_sea, dr_sea.index[-1]),
        plot_bgcolor = 'lightgray',
    )
    return {'data': data, 'layout': layout}

@app.callback(
    Output('daily-rankings', 'children'),
    [Input('df-fdta', 'children'),
    Input('selected-sea', 'value'),
    Input('product', 'value')])
def daily_ranking(df_fdta, selected_sea, selected_product):
    print(selected_sea)
    df_fdta = pd.read_json(df_fdta)
    dr = df_fdta[(df_fdta.index.month == df_fdta.index[-1].month) & (df_fdta.index.day == df_fdta.index[-1].day)]
    # print(dr)
    dr_sea = dr[selected_sea]
    sort_dr_sea = dr_sea.sort_values(axis=0, ascending=True)
    sort_dr_sea = pd.DataFrame({'km2':sort_dr_sea.values, 'YEAR':sort_dr_sea.index.year})
    sort_dr_sea = sort_dr_sea.round(0)
    # print(sort_dr_sea)
    if selected_product == 'extent-stats':
        return html.Div([
                html.Div('Current Day Values', style={'text-align': 'center'}),
                html.Div([
                    html.Div([
                        html.Div([
                            html.Div('{}'.format(sort_dr_sea.YEAR[i]), style={'text-align': 'center'}) for i in range(10)
                        ],
                            className='eight columns'
                        ),
                        html.Div([
                            html.Div('{:,.0f}'.format(sort_dr_sea.iloc[i,0]), style={'text-align': 'left'}) for i in range(10)
                        ],
                            className='four columns'
                        ),  
                    ],
                        className='row'
                    ),
                ],
                    className='round1'
                ),      
            ],
                className='round1'
            )

@app.callback(
    Output('annual-rankings', 'children'),
    [Input('product', 'value')])
def annual_ranking(selected_product):
    df1 = df['Total Arctic Sea']

    x = 0

    rankings = [['2006', 0],['2007', 0],['2008', 0],['2009', 0],['2010', 0],['2011', 0],['2012', 0],['2013', 0],['2014', 0],['2015', 0],['2016', 0],['2017', 0],['2018', 0],['2019', 0]]
    rank = pd.DataFrame(rankings, columns = ['Year','Pts'])
    
    while x < 366:
        dr1 = df1[(df1.index.month == df1.index[x].month) & (df1.index.day == df1.index[x].day)]
        dr_sort = dr1.sort_values(axis=0, ascending=True)
    
        rank.loc[rank['Year'] == str(dr_sort.index.year[0]), 'Pts'] += 10
        rank.loc[rank['Year'] == str(dr_sort.index.year[1]), 'Pts'] += 9
        rank.loc[rank['Year'] == str(dr_sort.index.year[2]), 'Pts'] += 8
        rank.loc[rank['Year'] == str(dr_sort.index.year[3]), 'Pts'] += 7
        rank.loc[rank['Year'] == str(dr_sort.index.year[4]), 'Pts'] += 6
        rank.loc[rank['Year'] == str(dr_sort.index.year[5]), 'Pts'] += 5
        rank.loc[rank['Year'] == str(dr_sort.index.year[6]), 'Pts'] += 4
        rank.loc[rank['Year'] == str(dr_sort.index.year[7]), 'Pts'] += 3
        rank.loc[rank['Year'] == str(dr_sort.index.year[8]), 'Pts'] += 2
        rank.loc[rank['Year'] == str(dr_sort.index.year[9]), 'Pts'] += 1
       
        rank.sort_values(by=['Pts'], ascending=True)
        x += 1

    sorted_rank = rank.sort_values('Pts', ascending=False)
    # print(rank)

    if selected_product == 'extent-stats':
        return html.Div([
                html.Div('Annual Ranks', style={'text-align': 'center'}),
                html.Div([
                    html.Div([
                        html.Div([
                            html.Div('{}'.format(sorted_rank.iloc[y][0]), style={'text-align': 'center'}) for y in range(0,14)
                        ],
                            className='eight columns'
                        ),
                        html.Div([
                            html.Div('{:,}'.format(sorted_rank.iloc[y,1]), style={'text-align': 'left'}) for y in range(0,14)
                        ],
                            className='four columns'
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
    Output('df-fdta', 'children'),
    [Input('product', 'value')])
def display_stats(selected_product):
    df_fdta = df.rolling(window=5).mean()
    if selected_product == 'extent-stats' or selected_product == 'years-graph':
        return df_fdta.to_json()

@app.callback(
    Output('bar-stats', 'children'),
    [Input('df-monthly', 'children'),
    Input('product','value')])
def display_graph_stats(ice, selected_product):
    df_monthly = pd.read_json(ice)
    extent = df_monthly['data'].apply(pd.Series)
    extent['value'] = extent['value'].astype(float)
    extent = extent.sort_values('value')
    extent = extent[extent.value != -9999]

    if selected_product == 'monthly-bar':
        return html.Div([
                html.Div('10 Lowest Extents for Selected Month', style={'text-align': 'center'}),
                html.Div([
                    html.Div([
                        html.Div([
                            html.Div('{}'.format(extent.index[i]), style={'text-align': 'center'}) for i in range(10)
                        ],
                            className='eight columns'
                        ),
                        html.Div([
                            html.Div('{}'.format(extent.iloc[i,0]), style={'text-align': 'left'}) for i in range(10)
                        ],
                            className='four columns'
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
        return html.P('Select Years') , html.Div([
            dcc.Checklist(
            id='selected-years',
            options=year_options,       
            )
        ],
            className='pretty_container'
        )

@app.callback(
    Output('sea-selector', 'children'),
    [Input('product', 'value')])
def display_sea_selector(product_value):
    if product_value == 'years-graph' or product_value == 'extent-stats':
        return html.P('Select Sea') ,dcc.Dropdown(
            id='selected-sea',
            options=sea_options,
            value='Total Arctic Sea'      
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
    elif value == 'extent-stats':
        return dcc.Graph(id='daily-rankings-graph')

@app.callback(
    Output('current-stats', 'children'),
    [Input('selected-sea', 'value'),
    Input('product', 'value'),
    Input('df-fdta', 'children')])
def update_current_stats(selected_sea, selected_product, df_fdta):
    df_fdta = pd.read_json(df_fdta)
    current_value = df_fdta[selected_sea][-1]
    print(df_fdta)
    if selected_product == 'years-graph':
        return html.Div([
                html.Div('Current Extent', style={'text-align': 'center'}),
                html.Div([
                    html.Div([
                        html.Div([
                            html.Div('{:,.0f}'.format(current_value), style={'text-align': 'center'}) 
                        ],
                            className='twelve columns'
                        ),
                    #     html.Div([
                    #         html.Div('{}'.format(extent.iloc[i,0]), style={'text-align': 'left'}) for i in range(10)
                    #     ],
                    #         className='four columns'
                    #     ),  
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
    Output('ice-extent', 'figure'),
    [Input('selected-sea', 'value'),
    Input('selected-years', 'value'),
    Input('df-fdta', 'children')])
def update_figure(selected_sea, selected_year, df_fdta):
    traces = []
    df_fdta = pd.read_json(df_fdta)
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
def update_figure_c(month_value):
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
