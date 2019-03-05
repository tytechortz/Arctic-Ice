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

df = pd.read_csv('ftp://sidads.colorado.edu/DATASETS/NOAA/G02186/masie_4km_allyears_extent_sqkm.csv', skiprows=1)
df10 = pd.read_csv('ftp://sidads.colorado.edu/DATASETS/NOAA/G02186/masie_4km_allyears_extent_sqkm.csv', skiprows=1)



df['yyyyddd'] = pd.to_datetime(df['yyyyddd'], format='%Y%j')
df['datetime']= pd.to_datetime(df['yyyyddd'])

df = df.set_index('datetime')


value_range = [0, 365]

year_options = []

for YEAR in df.index.year.unique():
    year_options.append({'label':(YEAR), 'value':YEAR})


today_value = df[' (0) Northern_Hemisphere'].iloc[-5:].mean(axis=0)
print(today_value)
yesterday_value = df[' (0) Northern_Hemisphere'].iloc[-6:-1].mean(axis=0)
print(yesterday_value)
week_ago_value = df[' (0) Northern_Hemisphere'].iloc[-11:-6].mean(axis=0)
print(week_ago_value)
weekly_change = today_value - week_ago_value
daily_difference = today_value - yesterday_value
# daily_difference = df[' (0) Northern_Hemisphere'].iloc[-1] - df[' (0) Northern_Hemisphere'].iloc[-2]
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

count_row = df10.shape[0]
days = count_row


year = datetime.datetime.now().year
annual_maximums = df2[' (0) Northern_Hemisphere'].loc[df2.groupby(pd.Grouper(freq='Y')).idxmax().iloc[:-1, 0]]
current_year_df = df[' (0) Northern_Hemisphere'][df[' (0) Northern_Hemisphere'].index.year == year]
current_year_max = current_year_df.max()
change_from_current_year_max = today_value - current_year_max

# Rankings by day of year
today = datetime.datetime.today()
yesterday = datetime.datetime.today() - datetime.timedelta(days=1)
y_day = yesterday.strftime("%d")
y_mon = yesterday.strftime("%m")
y_day_int = int(y_day)
y_mon_int = int(y_mon)

df11 = df2[' (0) Northern_Hemisphere']

df_daily_rankings = df11[(df11.index.month == y_mon_int) & (df11.index.day == y_day_int)]
sorted_daily_rankings = df_daily_rankings.sort_values(axis=0, ascending=False)
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
                    html.H5('Record Minimum: {:,.1f} km2'.format(record_min[0])),
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
                    html.H5('Low Max: {:,.1f} km2, {}'.format(df_min_max, df3.index[0].year)),
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
                    html.H6("1- {:,.1f} km2,  {}".format(df4[13], df4.index[13].year)),
                ]),
                width={'size':4},
                style={'text-align':'center'}
            ),
            dbc.Col(
                html.Div([
                    html.H6("1- {:,.1f} km2,  {}".format(df5[13], df5.index[13].year)),
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
                    html.H6("2- {:,.1f} km2,  {}".format(df4[12], df4.index[12].year)),
                ]),
                width={'size':4},
                style={'text-align':'center'} 
            ),
            dbc.Col(
                html.Div([
                    html.H6("2- {:,.1f} km2,  {}".format(df5[12], df5.index[12].year)),
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
                    html.H6("3- {:,.1f} km2,  {}".format(df4[11], df4.index[11].year)),
                ]),
                width={'size':4},
                style={'text-align':'center'}
            ),
            dbc.Col(
                html.Div([
                    html.H6("3- {:,.1f} km2,  {}".format(df5[11], df5.index[11].year)),
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
                    html.H6("4- {:,.1f} km2,  {}".format(df4[10], df4.index[10].year)),
                ]),
                width={'size':4},
                style={'text-align':'center'} 
            ),
            dbc.Col(
                html.Div([
                    html.H6("4- {:,.1f} km2,  {}".format(df5[10], df5.index[10].year)),
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
                    html.H6("5- {:,.1f} km2,  {}".format(df4[9], df4.index[9].year)),
                ]),
                width={'size':4},
                style={'text-align':'center'} 
            ),
            dbc.Col(
                html.Div([
                    html.H6("5- {:,.1f} km2,  {}".format(df5[9], df5.index[9].year)),
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
                    html.H6("6- {:,.1f} km2,  {}".format(df4[8], df4.index[8].year)),
                ]),
                width={'size':4},
                style={'text-align':'center'}
            ),
            dbc.Col(
                html.Div([
                    html.H6("6- {:,.1f} km2,  {}".format(df5[8], df5.index[8].year)),
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
                    html.H6("7- {:,.1f} km2,  {}".format(df4[7], df4.index[7].year)),
                ]),
                width={'size':4},
                style={'text-align':'center'} 
            ),
            dbc.Col(
                html.Div([
                    html.H6("7- {:,.1f} km2,  {}".format(df5[7], df5.index[7].year)),
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
                    html.H6("8- {:,.1f} km2,  {}".format(df4[6], df4.index[6].year)),
                ]),
                width={'size':4},
                style={'text-align':'center'} 
            ),
            dbc.Col(
                html.Div([
                    html.H6("8- {:,.1f} km2,  {}".format(df5[6], df5.index[6].year)),
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
                    html.H6("9- {:,.1f} km2,  {}".format(df4[5], df4.index[5].year)),
                ]),
                width={'size':4},
                style={'text-align':'center'} 
            ),
            dbc.Col(
                html.Div([
                    html.H6("9- {:,.1f} km2,  {}".format(df5[5], df5.index[5].year)),
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
                    html.H6("10- {:,.1f} km2,  {}".format(df4[4], df4.index[4].year)),
                ]),
                width={'size':4},
                style={'text-align':'center'} 
            ),
            dbc.Col(
                html.Div([
                    html.H6("10- {:,.1f} km2,  {}".format(df5[4], df5.index[4].year)),
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
        dbc.Row([
            dbc.Col(
                html.Div(
                    html.H5('Daily Ice Extent: 2006-Present', style={'text-align': 'center', 'color': 'black'}),
                ),
                width={'size':4},
                style={'text-align':'center'}
            ),
        ],
        justify='around'
        ),
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
                                    'name' : 'Ice'
                                },
                                {
                                    'x' : df.index,
                                    'y' : all_ice_fit(),
                                    'name' : 'Trend'
                                }
                            ],
                            'layout': go.Layout(
                                xaxis = {'title': ''},
                                yaxis = {'title': 'Ice Extent km2'},
                                hovermode = 'closest',
                                height = 500, 
                                title = 'Arctic Sea Ice Extent'    
                            ), 
                        }
                    ),
                ]),
                width = {'size':10},
            ), 
        ],
        justify='around'
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