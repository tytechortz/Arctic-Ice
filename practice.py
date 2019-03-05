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

# Read data
df = pd.read_csv('ftp://sidads.colorado.edu/DATASETS/NOAA/G02186/masie_4km_allyears_extent_sqkm.csv', skiprows=1)
# Format date and set indext to date
df['yyyyddd'] = pd.to_datetime(df['yyyyddd'], format='%Y%j')
df.set_index('yyyyddd', inplace=True)

# Change dataframe to 5 day trailing average
df_fdta = df.rolling(window=5).mean()

# Current day's value- 5 day trailing mean
today_value = df_fdta[' (0) Northern_Hemisphere'].iloc[-1]

#  Yesterday's value-5 day trailing mean
yesterday_value = df_fdta[' (0) Northern_Hemisphere'].iloc[-1]

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

# Rankings by day of year
today = datetime.datetime.today()
yesterday = datetime.datetime.today() - datetime.timedelta(days=1)
y_day = yesterday.strftime("%d")
y_mon = yesterday.strftime("%m")
y_day_int = int(y_day)
y_mon_int = int(y_mon)

df10 = df[' (0) Northern_Hemisphere']
df_daily_rankings = df10[(df10.index.month == y_mon_int) & (df10.index.day == y_day_int)]
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
    ])
])



app.layout = html.Div(body)

if __name__ == "__main__":
    app.run_server(port=8124, debug=True)