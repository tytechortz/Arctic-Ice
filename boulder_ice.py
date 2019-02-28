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
from scipy.stats import norm



app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config['suppress_callback_exceptions']=True

pd.options.display.float_format = '{:,}'.format

df = pd.read_csv('ftp://sidads.colorado.edu/DATASETS/NOAA/G02186/masie_4km_allyears_extent_sqkm.csv', skiprows=1)
df10 = pd.read_csv('ftp://sidads.colorado.edu/DATASETS/NOAA/G02186/masie_4km_allyears_extent_sqkm.csv', skiprows=1)



df['yyyyddd'] = pd.to_datetime(df['yyyyddd'], format='%Y%j')
df['datetime']= pd.to_datetime(df['yyyyddd'])

df = df.set_index('datetime')


value_range = [0, 365]

year_options = []
# for YEAR in df['yyyyddd'].dt.strftime('%Y').unique():
for YEAR in df.index.year.unique():
    year_options.append({'label':(YEAR), 'value':YEAR})

# df2=df[(df['yyyyddd'].dt.year == 2017)]


today_value = df[' (0) Northern_Hemisphere'].iloc[-1]
week_ago_value = df[' (0) Northern_Hemisphere'].iloc[-7]
weekly_change = today_value - week_ago_value
daily_difference = df[' (0) Northern_Hemisphere'].iloc[-1] - df[' (0) Northern_Hemisphere'].iloc[-2]
record_min = df[' (0) Northern_Hemisphere'].min(),
df[' (0) Northern_Hemisphere'].iloc[-1]
record_min_difference = today_value - record_min[0]
record_max = df[' (0) Northern_Hemisphere'].max(),
record_max_difference = today_value - record_max[0]




df2=pd.read_csv('ftp://sidads.colorado.edu/DATASETS/NOAA/G02186/masie_4km_allyears_extent_sqkm.csv', skiprows=1)
df2['yyyyddd'] = pd.to_datetime(df2['yyyyddd'], format='%Y%j')
df2.set_index('yyyyddd', inplace=True)
df3 = df2[' (0) Northern_Hemisphere'].loc[df2.groupby(pd.Grouper(freq='Y')).idxmax().iloc[:, 0]]
df4 = df3.sort_values(axis=0, ascending=False)
df_min = df2[' (0) Northern_Hemisphere'].loc[df2.groupby(pd.Grouper(freq='Y')).idxmin().iloc[:, 0]]
df5 = df_min.sort_values(axis=0, ascending=False)

df_min_max = df3[0]
record_low_max_difference = today_value - df_min_max

startyr = 2006
presentyr = datetime.now().year
year_count = presentyr-startyr

count_row = df10.shape[0]
days = count_row

annual_maximums = df2[' (0) Northern_Hemisphere'].loc[df2.groupby(pd.Grouper(freq='Y')).idxmax().iloc[:-1, 0]]

# Rankings by day of year
current_month = datetime.now().month
current_day = datetime.now().day
yesterday = current_day -1
df11 = df2[' (0) Northern_Hemisphere']
df_daily_rankings = df11[(df11.index.month == current_month) & (df11.index.day == yesterday)]
sorted_daily_rankings = df_daily_rankings.sort_values(axis=0, ascending=False)
# drl = daily rankings length
drl = sorted_daily_rankings.size


def all_ice_fit():
    xi = arange(0,days)
    slope, intercept, r_value, p_value, std_err = stats.linregress(xi,df10[" (0) Northern_Hemisphere"])
    return (slope*xi+intercept)

body = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(
                html.Div(
                    className="app-header",
                    children=[
                        html.Div('Arctic Sea Ice Extent', className="app-header--title"),
                    ]
                ),
            ),
        ]),
        dbc.Row([
            dbc.Col(
                html.Div(
                    html.H3('2006-Present', style={'text-align': 'center'}),
                ),
                width={'size': 8, 'offset': 2}
            ),
        ]),
        dbc.Row([
            dbc.Col(
                html.Div(
                    html.H3('Data From National Snow and Ice Data Center', style={'text-align': 'center'}),
                ),
                width={'size': 6, 'offset': 3}
            ),
        ]),
        dbc.Row(
            [
            dbc.Col(
                html.Div(
                    dcc.Graph(id='ice-extent', style={'height':700}),    
                ),
                width={'size':12}
                ),
        ],
        justify='around'
        ),
        dbc.Row([
            dbc.Col(
                html.Div(
                    html.H2('Select Years', style={'text-align': 'center', 'color': 'black'}),
                ),
                width={'size': 6, 'offset': 3}
            ),
        ]),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Dropdown(id='year1',options=year_options
                    ), 
                    width={'size':2, 'offset':2}
                ),
                dbc.Col(
                    dcc.Dropdown(id='year2',options=year_options
                    ),
                    width={'size':2} 
                ),
                dbc.Col(
                    dcc.Dropdown(id='year3',options=year_options
                    ),
                    width={'size':2} 
                ),
                dbc.Col(
                    dcc.Dropdown(id='year4',options=year_options
                    ),
                    width={'size':2} 
                ),
            ],
        ),
        dbc.Row([
            dbc.Col(
                html.Div([
                ]),
                style={'height':25, 'align':'end'} 
            ), 
        ]),
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.H2("Today's Value: {:,.1f} km2".format(today_value)),
                ]),
                width={'size':5,'offset':1},
                style={'height':40, 'align':'start'} 
            ),
            dbc.Col(
                html.Div([
                    html.H2('Record Minimum: {:,.1f} km2'.format(record_min[0])),
                ]),
                width={'size':5, 'offset':1},
                style={'height':40, 'align':'start'} 
            ), 
        ]),
        dbc.Row([
            dbc.Col(
                html.Div([
                     html.H2("24 Hour Change: {:,.1f} km2".format(daily_difference)),
                ]),
                width={'size':5,'offset':1},
                style={'height':40, 'align':'end'} 
            ),
            dbc.Col(
                html.Div([
                    html.H2('Difference: {:,.1f} km2'.format(record_min_difference)),
                ]),
                width={'size':5,'offset':1},
                style={'height':40, 'align':'start'} 
            ), 
        ]),
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.H2('Maximum: {:,.1f} km2, {}'.format(record_max[0], df4.index[0].year)),
                ]),
                width={'size':5,'offset':1},
                style={'height':40, 'align':'end'} 
            ),
            dbc.Col(
                html.Div([
                    html.H2('Low Max: {:,.1f} km2, {}'.format(df_min_max, df3.index[0].year)),
                ]),
                width={'size':5,'offset':1},
                style={'height':40, 'align':'start'} 
            ),  
        ]),
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.H2('Weekly Change: {:,.1f} km2'.format(weekly_change)),
                ]),
                width={'size':5,'offset':1},
                style={'height':40, 'align':'start'} 
            ),
            dbc.Col(
                html.Div([
                    html.H2('Difference: {:,.1f} km2'.format(record_low_max_difference)),
                ]),
                width={'size':5,'offset':1},
                style={'height':40, 'align':'start'} 
            ), 
        ]),
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.H2('Lowest Annual Maximums',style={'color': 'black','font-size':40}),
                ]),
                style={'height':40, 'align':'start'} 
            ),
            dbc.Col(
                html.Div([
                    html.H2('Annual Minimums',style={'color': 'black','font-size':40}),
                ]),
                style={'height':40, 'align':'start'} 
            ),
            dbc.Col(
                html.Div([
                    html.H2('Values Current Date',style={'color': 'black','font-size':40}),
                ]),
                style={'height':40, 'align':'start'} 
            ),
        ]),
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.H2("1- {:,.1f} km2,  {}".format(df4[13], df4.index[13].year)),
                ])
            ),
            dbc.Col(
                html.Div([
                    html.H2("1- {:,.1f} km2,  {}".format(df5[13], df5.index[13].year)),
                ])
            ),
            dbc.Col(
                html.Div([
                    html.H2("1- {:,.1f} km2,  {}".format(sorted_daily_rankings[drl-1], sorted_daily_rankings.index[drl-1].year)),
                ])
            )
        ]),

        dbc.Row([
            dbc.Col(
                html.Div([
                    html.H2("2- {:,.1f} km2,  {}".format(df4[12], df4.index[12].year)),
                ]),
                style={'height':40, 'align':'start'} 
            ),
            dbc.Col(
                html.Div([
                    html.H2("2- {:,.1f} km2,  {}".format(df5[12], df5.index[12].year)),
                ])
            ),
            dbc.Col(
                html.Div([
                    html.H2("2- {:,.1f} km2,  {}".format(sorted_daily_rankings[drl-2], sorted_daily_rankings.index[drl-2].year)),
                ])
            ) 
        ]),
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.H2("3- {:,.1f} km2,  {}".format(df4[11], df4.index[11].year)),
                ]),
                style={'height':40, 'align':'start'} 
            ),
            dbc.Col(
                html.Div([
                    html.H2("3- {:,.1f} km2,  {}".format(df5[11], df5.index[11].year)),
                ])
            ),
            dbc.Col(
                html.Div([
                    html.H2("3- {:,.1f} km2,  {}".format(sorted_daily_rankings[drl-3],sorted_daily_rankings.index[drl-3].year)),
                ])
            ) 
        ]),
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.H2("4- {:,.1f} km2,  {}".format(df4[10], df4.index[10].year)),
                ]),
                style={'height':40, 'align':'start'} 
            ),
            dbc.Col(
                html.Div([
                    html.H2("4- {:,.1f} km2,  {}".format(df5[10], df5.index[10].year)),
                ])
            ),
            dbc.Col(
                html.Div([
                    html.H2("4- {:,.1f} km2,  {}".format(sorted_daily_rankings[drl-4], sorted_daily_rankings.index[drl-4].year)),
                ])
            ) 
        ]),
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.H2("5- {:,.1f} km2,  {}".format(df4[9], df4.index[9].year)),
                ]),
                style={'height':40, 'align':'start'} 
            ),
            dbc.Col(
                html.Div([
                    html.H2("5- {:,.1f} km2,  {}".format(df5[9], df5.index[9].year)),
                ])
            ),
            dbc.Col(
                html.Div([
                    html.H2("5- {:,.1f} km2,  {}".format(sorted_daily_rankings[drl-5], sorted_daily_rankings.index[drl-5].year)),
                ])
            ) 
        ]),
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.H2("6- {:,.1f} km2,  {}".format(df4[8], df4.index[8].year)),
                ]),
                style={'height':40, 'align':'start'} 
            ),
            dbc.Col(
                html.Div([
                    html.H2("6- {:,.1f} km2,  {}".format(df5[8], df5.index[8].year)),
                ])
            ),
            dbc.Col(
                html.Div([
                    html.H2("6- {:,.1f} km2,  {}".format(sorted_daily_rankings[drl-6], sorted_daily_rankings.index[drl-6].year)),
                ])
            ) 
        ]),
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.H2("7- {:,.1f} km2,  {}".format(df4[7], df4.index[7].year)),
                ]),
                style={'height':40, 'align':'start'} 
            ),
            dbc.Col(
                html.Div([
                    html.H2("7- {:,.1f} km2,  {}".format(df5[7], df5.index[7].year)),
                ])
            ),
            dbc.Col(
                html.Div([
                    html.H2("7- {:,.1f} km2,  {}".format(sorted_daily_rankings[drl-7], sorted_daily_rankings.index[drl-7].year)),
                ])
            ) 
        ]),
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.H2("8- {:,.1f} km2,  {}".format(df4[6], df4.index[6].year)),
                ]),
                style={'height':40, 'align':'start'} 
            ),
            dbc.Col(
                html.Div([
                    html.H2("8- {:,.1f} km2,  {}".format(df5[6], df5.index[6].year)),
                ])
            ),
            dbc.Col(
                html.Div([
                    html.H2("8- {:,.1f} km2,  {}".format(sorted_daily_rankings[drl-8], sorted_daily_rankings.index[drl-8].year)),
                ])
            ) 
        ]),
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.H2("9- {:,.1f} km2,  {}".format(df4[5], df4.index[5].year)),
                ]),
                style={'height':40, 'align':'start'} 
            ),
            dbc.Col(
                html.Div([
                    html.H2("9- {:,.1f} km2,  {}".format(df5[5], df5.index[5].year)),
                ])
            ),
            dbc.Col(
                html.Div([
                    html.H2("9- {:,.1f} km2,  {}".format(sorted_daily_rankings[drl-9], sorted_daily_rankings.index[drl-9].year)),
                ])
            ) 
        ]),
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.H2("10- {:,.1f} km2,  {}".format(df4[4], df4.index[4].year)),
                ]),
                style={'height':40, 'align':'start'} 
            ),
            dbc.Col(
                html.Div([
                    html.H2("10- {:,.1f} km2,  {}".format(df5[4], df5.index[4].year)),
                ])
            ),
            dbc.Col(
                html.Div([
                    html.H2("10- {:,.1f} km2,  {}".format(sorted_daily_rankings[drl-10], sorted_daily_rankings.index[drl-10].year)),
                ])
            ) 
        ]),
        dbc.Row([
            dbc.Col(
                html.Div(
                    html.H2('Daily Ice Extent:2006-Present', style={'text-align': 'center', 'color': 'black'}),
                ),
                width={'size': 6, 'offset': 3}
            ),
        ]),
        dbc.Row(
        [
           dbc.Col(
                html.Div([
                    dcc.Graph(id='all-ice',  
                        figure = {
                            'data': [
                                {
                                    'x' : df.index, 
                                    'y' : df[' (0) Northern_Hemisphere'],
                                    'mode' : 'lines + markers',
                                    'name' : 'Max Temp'
                                },
                                {
                                    'x' : df.index,
                                    'y' : all_ice_fit(),
                                    'name' : 'trend'
                                }
                            ],
                            'layout': go.Layout(
                                xaxis = {'title': ''},
                                yaxis = {'title': 'Ice Extent km2'},
                                hovermode = 'closest',
                                height = 1000     
                            ), 
                        }
                    ),
                ]),
                width = {'size':12},
            ), 
        ]
    ),
    ]),
])


      


html.Ul([html.Li(x) for x in annual_maximums.sort_values(ascending=True)]) 

@app.callback(
    Output('ice-extent', 'figure'),
    [Input('year1', 'value'),
    Input('year2', 'value'),
    Input('year3', 'value'),
    Input('year4', 'value'),])
def update_figure(selected_year1,selected_year2, selected_year3, selected_year4):
    traces = []
    selected_years = [selected_year1,selected_year2,selected_year3,selected_year4]
    for year in selected_years:
        df5=df[df.index.year == year]
        traces.append(go.Scatter(
            # x=df2['yyyyddd'],
            y=df5[' (0) Northern_Hemisphere'],
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