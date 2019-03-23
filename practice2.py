import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import pandas as pd
import sqlite3
from dash.dependencies import Input, Output
import time
import datetime
from pandas import Series
from scipy import stats 
from numpy import arange,array,ones 
from scipy.stats import norm
from pandas import DatetimeIndex

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config['suppress_callback_exceptions']=True

pd.options.display.float_format = '{:,}'.format

value_range = [0, 365]



# Read data
df = pd.read_csv('ftp://sidads.colorado.edu/DATASETS/NOAA/G02186/masie_4km_allyears_extent_sqkm.csv', skiprows=1)
# Format date and set indext to date
df['yyyyddd'] = pd.to_datetime(df['yyyyddd'], format='%Y%j')
df.set_index('yyyyddd', inplace=True)

# Dropdown year selector values
year_options = []
for YEAR in df.index.year.unique():
    year_options.append({'label':(YEAR), 'value':YEAR})

# Change dataframe to 5 day trailing average
df_fdta = df.rolling(window=5).mean()

# Current day's value- 5 day trailing mean
today_value = df_fdta[' (0) Northern_Hemisphere'].iloc[-1]

#  Yesterday's value-5 day trailing mean
yesterday_value = df_fdta[' (0) Northern_Hemisphere'].iloc[-2]

#  1 week ago 5 day trailing mean
week_ago_value = df_fdta[' (0) Northern_Hemisphere'].iloc[-7]


weekly_change = today_value - week_ago_value
daily_difference = today_value - yesterday_value

# Record minimum
record_min = df_fdta[' (0) Northern_Hemisphere'].min()

record_min_difference = today_value - record_min


record_max = df_fdta[' (0) Northern_Hemisphere'].max()


annual_max_all = df_fdta[' (0) Northern_Hemisphere'].loc[df_fdta.groupby(pd.Grouper(freq='Y')).idxmax().iloc[:, 0]]


sorted_annual_max_all = annual_max_all.sort_values(axis=0, ascending=False)


annual_min_all = df_fdta[' (0) Northern_Hemisphere'].loc[df_fdta.groupby(pd.Grouper(freq='Y')).idxmin().iloc[:, 0]]


sorted_annual_min_all = annual_min_all.sort_values(axis=0, ascending=False)

# Lowest annual max
low_max = annual_max_all[0]


record_low_max_difference = today_value - low_max

count_row = df.shape[0]
days = count_row

year = datetime.datetime.now().year
annual_maximums = df_fdta[' (0) Northern_Hemisphere'].loc[df_fdta.groupby(pd.Grouper(freq='Y')).idxmax().iloc[:-1, 0]]
current_year_df = df_fdta[' (0) Northern_Hemisphere'][df_fdta[' (0) Northern_Hemisphere'].index.year == year]
current_year_max = current_year_df.max()
change_from_current_year_max = today_value - current_year_max

# Rankings by last 5 dates of data
df10 = df_fdta[' (0) Northern_Hemisphere']
df_daily_rankings = df10[(df10.index.month == df.index.month[-1]) & (df10.index.day == df.index.day[-1])]
sorted_daily_rankings = df_daily_rankings.sort_values(axis=0, ascending=False)
drl = sorted_daily_rankings.size


# Linear trendline
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
                    html.H6('2006-Present', style={'text-align': 'center'}),
                ),
                width={'size': 8, 'offset': 2}
            ),
        ]),
        dbc.Row([
            dbc.Col(
                html.Div(
                    html.H6('Data From National Snow and Ice Data Center', style={'text-align': 'center'}),
                ),
                width={'size': 6, 'offset': 3}
            ),
        ]),
        dbc.Row([
            dbc.Col(
                html.Div(
                    html.H6('Select Sea', style={'text-align': 'center'}),
                ),
                width={'size': 6, 'offset': 3}
            ),
        ]),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Dropdown(id='sea',options=year_options
                    ), 
                    width={'size':4, 'offset':4},
                ),
            ],
            style={'height':30}
        ),
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        html.H6('', style={'text-align': 'center'}),
                    ),
                ),
            ],
            style={'height':30}
        ),
        dbc.Row(
            [
            dbc.Col(
                html.Div(
                    dcc.Graph(id='ice-extent', style={'height':450}),    
                ),
                width={'size':10}
                ),
            ],
        justify='around'
        ),
        dbc.Row([
            dbc.Col(
                html.Div(
                    html.H6('Select Years', style={'text-align': 'center', 'color': 'black'}),
                ),
                width={'size': 6, 'offset': 3}
            ),
        ]),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Dropdown(id='year1',options=year_options
                    ), 
                    width={'size':2, 'offset':2},
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
            style={'height':20}
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
                    html.H5("Today's Value: {:,.1f} km2".format(today_value)),
                ]),
                width={'size':6},
                style={'height':30, 'text-align':'center'} 
            ),
            dbc.Col(
                html.Div([
                    html.H5('Record Minimum: {:,.1f} km2'.format(record_min)),
                ]),
                width={'size':6},
                style={'height':30, 'text-align':'left'} 
            ), 
        ]),
        dbc.Row([
            dbc.Col(
                html.Div([
                     html.H5("24 Hour Change: {:,.1f} km2".format(daily_difference)),
                ]),
                width={'size':6},
                style={'height':30, 'text-align':'center'} 
            ),
            dbc.Col(
                html.Div([
                    html.H5('Difference: {:,.1f} km2'.format(record_min_difference)),
                ]),
                width={'size':6},
                style={'height':30, 'text-align':'left'} 
            ), 
        ]),
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.H5('Weekly Change: {:,.1f} km2'.format(weekly_change)),
                ]),
                width={'size':6},
                style={'height':30, 'text-align':'center'} 
            ),
            dbc.Col(
                html.Div([
                    html.H5('Low Max: {:,.1f} km2, {}'.format(low_max, sorted_annual_max_all.index[-1].year)),
                ]),
                width={'size':6},
                style={'height':30, 'text-align':'left'} 
            ),  
        ]),
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.H5('Change From Max: {:,.1f} km2, '.format(change_from_current_year_max)),
                ]),
                width={'size':6},
                style={'height':30, 'text-align':'center'} 
            ),
            dbc.Col(
                html.Div([
                    html.H5('Difference: {:,.1f} km2'.format(record_low_max_difference)),
                ]),
                width={'size':6},
                style={'height':30, 'text-align':'left'} 
            ), 
        ]),
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.H5('Lowest Annual Maximums',style={'color': 'black','font-size':20}),
                ]),
                width={'size':4},
                style={'height':30, 'text-align':'center'} 
            ),
            dbc.Col(
                html.Div([
                    html.H5('Annual Minimums',style={'color': 'black','font-size':20}),
                ]),
                width={'size':4},
                style={'height':30, 'text-align':'center'} 
            ),
            dbc.Col(
                html.Div([
                    html.H5('Values Current Date',style={'color': 'black','font-size':20}),
                ]),
                width={'size':4},
                style={'height':30, 'text-align':'center'}
            ),
        ]),
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.H6("1- {:,.1f} km2,  {}".format(sorted_annual_max_all[13], sorted_annual_max_all.index[13].year)),
                ]),
                width={'size':4},
                style={'text-align':'center'}
            ),
            dbc.Col(
                html.Div([
                    html.H6("1- {:,.1f} km2,  {}".format(sorted_annual_min_all[13], sorted_annual_min_all.index[13].year)),
                ]),
                width={'size':4},
                style={'text-align':'center'} 
            ),
            dbc.Col(
                html.Div([
                    html.H6("1- {:,.1f} km2,  {}".format(sorted_daily_rankings[drl-1], sorted_daily_rankings.index[drl-1].year)),
                ]),
                width={'size':4},
                style={'text-align':'center'}
            )
        ]),
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.H6("2- {:,.1f} km2,  {}".format(sorted_annual_max_all[12], sorted_annual_max_all.index[12].year)),
                ]),
                width={'size':4},
                style={'text-align':'center'} 
            ),
            dbc.Col(
                html.Div([
                    html.H6("2- {:,.1f} km2,  {}".format(sorted_annual_min_all[12], sorted_annual_min_all.index[12].year)),
                ]),
                width={'size':4},
                style={'text-align':'center'}
            ),
            dbc.Col(
                html.Div([
                    html.H6("2- {:,.1f} km2,  {}".format(sorted_daily_rankings[drl-2], sorted_daily_rankings.index[drl-2].year)),
                ]),
                width={'size':4},
                style={'text-align':'center'}
            ) 
        ]),
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.H6("3- {:,.1f} km2,  {}".format(sorted_annual_max_all[11], sorted_annual_max_all.index[11].year)),
                ]),
                width={'size':4},
                style={'text-align':'center'}
            ),
            dbc.Col(
                html.Div([
                    html.H6("3- {:,.1f} km2,  {}".format(sorted_annual_min_all[11], sorted_annual_min_all.index[11].year)),
                ]),
                width={'size':4},
                style={'text-align':'center'}
            ),
            dbc.Col(
                html.Div([
                    html.H6("3- {:,.1f} km2,  {}".format(sorted_daily_rankings[drl-3],sorted_daily_rankings.index[drl-3].year)),
                ]),
                width={'size':4},
                style={'text-align':'center'}
            ) 
        ]),
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.H6("4- {:,.1f} km2,  {}".format(sorted_annual_max_all[10], sorted_annual_max_all.index[10].year)),
                ]),
                width={'size':4},
                style={'text-align':'center'} 
            ),
            dbc.Col(
                html.Div([
                    html.H6("4- {:,.1f} km2,  {}".format(sorted_annual_min_all[10], sorted_annual_min_all.index[10].year)),
                ]),
                width={'size':4},
                style={'text-align':'center'}
            ),
            dbc.Col(
                html.Div([
                    html.H6("4- {:,.1f} km2,  {}".format(sorted_daily_rankings[drl-4], sorted_daily_rankings.index[drl-4].year)),
                ]),
                width={'size':4},
                style={'text-align':'center'}
            ) 
        ]),
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.H6("5- {:,.1f} km2,  {}".format(sorted_annual_max_all[9], sorted_annual_max_all.index[9].year)),
                ]),
                width={'size':4},
                style={'text-align':'center'} 
            ),
            dbc.Col(
                html.Div([
                    html.H6("5- {:,.1f} km2,  {}".format(sorted_annual_min_all[9], sorted_annual_min_all.index[9].year)),
                ]),
                width={'size':4},
                style={'text-align':'center'}
            ),
            dbc.Col(
                html.Div([
                    html.H6("5- {:,.1f} km2,  {}".format(sorted_daily_rankings[drl-5], sorted_daily_rankings.index[drl-5].year)),
                ]),
                width={'size':4},
                style={'text-align':'center'}
            ) 
        ]),
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.H6("6- {:,.1f} km2,  {}".format(sorted_annual_max_all[8], sorted_annual_max_all.index[8].year)),
                ]),
                width={'size':4},
                style={'text-align':'center'}
            ),
            dbc.Col(
                html.Div([
                    html.H6("6- {:,.1f} km2,  {}".format(sorted_annual_min_all[8], sorted_annual_min_all.index[8].year)),
                ]),
                width={'size':4},
                style={'text-align':'center'}
            ),
            dbc.Col(
                html.Div([
                    html.H6("6- {:,.1f} km2,  {}".format(sorted_daily_rankings[drl-6], sorted_daily_rankings.index[drl-6].year)),
                ]),
                width={'size':4},
                style={'text-align':'center'}
            ) 
        ]),
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.H6("7- {:,.1f} km2,  {}".format(sorted_annual_max_all[7], sorted_annual_max_all.index[7].year)),
                ]),
                width={'size':4},
                style={'text-align':'center'} 
            ),
            dbc.Col(
                html.Div([
                    html.H6("7- {:,.1f} km2,  {}".format(sorted_annual_min_all[7], sorted_annual_min_all.index[7].year)),
                ]),
                width={'size':4},
                style={'text-align':'center'}
            ),
            dbc.Col(
                html.Div([
                    html.H6("7- {:,.1f} km2,  {}".format(sorted_daily_rankings[drl-7], sorted_daily_rankings.index[drl-7].year)),
                ]),
                width={'size':4},
                style={'text-align':'center'}
            ) 
        ]),
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.H6("8- {:,.1f} km2,  {}".format(sorted_annual_max_all[6], sorted_annual_max_all.index[6].year)),
                ]),
                width={'size':4},
                style={'text-align':'center'} 
            ),
            dbc.Col(
                html.Div([
                    html.H6("8- {:,.1f} km2,  {}".format(sorted_annual_min_all[6], sorted_annual_min_all.index[6].year)),
                ]),
                width={'size':4},
                style={'text-align':'center'}
            ),
            dbc.Col(
                html.Div([
                    html.H6("8- {:,.1f} km2,  {}".format(sorted_daily_rankings[drl-8], sorted_daily_rankings.index[drl-8].year)),
                ]),
                width={'size':4},
                style={'text-align':'center'}
            ) 
        ]),
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.H6("9- {:,.1f} km2,  {}".format(sorted_annual_max_all[5], sorted_annual_max_all.index[5].year)),
                ]),
                width={'size':4},
                style={'text-align':'center'} 
            ),
            dbc.Col(
                html.Div([
                    html.H6("9- {:,.1f} km2,  {}".format(sorted_annual_min_all[5], sorted_annual_min_all.index[5].year)),
                ]),
                width={'size':4},
                style={'text-align':'center'}
            ),
            dbc.Col(
                html.Div([
                    html.H6("9- {:,.1f} km2,  {}".format(sorted_daily_rankings[drl-9], sorted_daily_rankings.index[drl-9].year)),
                ]),
                width={'size':4},
                style={'text-align':'center'}
            ) 
        ]),
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.H6("10- {:,.1f} km2,  {}".format(sorted_annual_max_all[4], sorted_annual_max_all.index[4].year)),
                ]),
                width={'size':4},
                style={'text-align':'center'} 
            ),
            dbc.Col(
                html.Div([
                    html.H6("10- {:,.1f} km2,  {}".format(sorted_annual_min_all[4], sorted_annual_min_all.index[4].year)),
                ]),
                width={'size':4},
                style={'text-align':'center'}
            ),
            dbc.Col(
                html.Div([
                    html.H6("10- {:,.1f} km2,  {}".format(sorted_daily_rankings[drl-10], sorted_daily_rankings.index[drl-10].year)),
                ]),
                width={'size':4},
                style={'text-align':'center'}
            ) 
        ]),
    ])
])

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
        sorted_daily_values=df_fdta[df_fdta.index.year == year]
        traces.append(go.Scatter(
            # x=df2['yyyyddd'],
            y=sorted_daily_values[' (0) Northern_Hemisphere'],
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