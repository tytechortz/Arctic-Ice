import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import pandas as pd
import sqlite3
from dash.dependencies import Input, Output
import time
from datetime import datetime
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
df.columns = ['Total Arctic Sea', 'Beaufort Sea', 'Chukchi Sea', 'East Siberian Sea', 'Laptev Sea', 'Kara Sea',\
     'Barents Sea', 'Greenland Sea', 'Bafin Bay Gulf of St. Lawrence', 'Canadian Archipelago', 'Hudson Bay', 'Central Arctic',\
         'Bering Sea', 'Baltic Sea', 'Sea of Okhotsk', 'Yellow Sea', 'Cook Inlet']

count_row = df.shape[0]
days = count_row

# Dropdown year selector values
year_options = []
for YEAR in df.index.year.unique():
    year_options.append({'label':(YEAR), 'value':YEAR})

# Dropdown sea selector values
sea_options = []
for sea in df.columns.unique():
    sea_options.append({'label':sea, 'value':sea})

# Change dataframe to 5 day trailing average
df_fdta = df.rolling(window=5).mean()

startyr = 2006
presentyr = datetime.now().year
year_count = presentyr-startyr

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
                    dcc.Dropdown(id='sea',options=sea_options
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
                    html.H6(id='current-value')
                ]),
                width={'size':6},
                style={'text-align':'center'}
            ),
            dbc.Col(
                html.Div([
                    html.H6(id='record-min'),
                ]),
                width={'size':6},
                style={'text-align':'center'}
            ),
        ]),
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.H6(id='daily-change')
                ]),
                width={'size':6},
                style={'text-align':'center'}
            ),
            dbc.Col(
                html.Div([
                    html.H6(id='record-min-difference'),
                ]),
                width={'size':6},
                style={'text-align':'center'}
            ),
        ]),
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.H6(id='weekly-change')
                ]),
                width={'size':6},
                style={'text-align':'center'}
            ),
            dbc.Col(
                html.Div([
                    html.H6(id='low-max'),
                ]),
                width={'size':6},
                style={'text-align':'center'}
            ),
        ]),
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.H6(id='max-diff')
                ]),
                width={'size':6},
                style={'text-align':'center'}
            ),
            dbc.Col(
                html.Div([
                    html.H6(id='daily-low-diff'),
                ]),
                width={'size':6},
                style={'text-align':'center'}
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
                html.Div(id='annual-max-table'),
            ),
            dbc.Col(
                html.Div(id='annual-min-table'),
            ),
            dbc.Col(
                html.Div(id='current-date-values'),
            ),
        ]),
        dbc.Row(
            [
            dbc.Col(
                html.Div(
                    dcc.Graph(id='all-ice-extent', style={'height':450}),    
                ),
                width={'size':10}
                ),
            ],
        justify='around'
        ),
        
    ])

])

@app.callback(
    Output('ice-extent', 'figure'),
    [Input('sea', 'value'),
    Input('year1', 'value'),
    Input('year2', 'value'),
    Input('year3', 'value'),
    Input('year4', 'value'),])
def update_figure(selected_sea,selected_year1,selected_year2, selected_year3, selected_year4):
    traces = []
    selected_years = [selected_year1,selected_year2,selected_year3,selected_year4]
    for year in selected_years:
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

@app.callback(
    Output('current-value', 'children'),
    [Input('sea', 'value')])
def current_ice(selected_sea):
    today_value = df_fdta[selected_sea].iloc[-1]
    return "Today's Value: {:,.0f} km2".format(today_value),

@app.callback(
    Output('record-min', 'children'),
    [Input('sea', 'value')])
def current_ice_a(selected_sea):
    annual_min_all = df_fdta[selected_sea].loc[df_fdta.groupby(pd.Grouper(freq='Y')).idxmin().iloc[:, 0]]
    sorted_annual_min_all = annual_min_all.sort_values(axis=0, ascending=False)
    record_min = df_fdta[selected_sea].min()
    return "Record Minimum: {:,.0f} km2 - {}".format(record_min, sorted_annual_min_all.index[-1].year),

@app.callback(
    Output('daily-change', 'children'),
    [Input('sea', 'value')])
def current_ice_b(selected_sea):
    today_value = df_fdta[selected_sea].iloc[-1]
    yesterday_value = df_fdta[selected_sea].iloc[-2]
    daily_change = today_value - yesterday_value
    return "24 Hour Change: {:,.0f} km2".format(daily_change)

@app.callback(
    Output('record-min-difference', 'children'),
    [Input('sea', 'value')])
def current_ice_c(selected_sea):
    today_value = df_fdta[selected_sea].iloc[-1]
    record_min = df_fdta[selected_sea].min()
    record_min_difference = today_value - record_min
    return "Difference From Record: {:,.0f} km2".format(record_min_difference)

@app.callback(
    Output('weekly-change', 'children'),
    [Input('sea', 'value')])
def current_ice_d(selected_sea):
    today_value = df_fdta[selected_sea].iloc[-1]
    week_ago_value = df_fdta[selected_sea].iloc[-7]
    weekly_change = today_value - week_ago_value
    return "Weekly Change: {:,.0f} km2".format(weekly_change)

@app.callback(
    Output('low-max', 'children'),
    [Input('sea', 'value')])
def current_ice_e(selected_sea):
    annual_max_all = df_fdta[selected_sea].loc[df_fdta.groupby(pd.Grouper(freq='Y')).idxmax().iloc[:, 0]]
    sorted_annual_max_all = annual_max_all.sort_values(axis=0, ascending=False)
    low_max = annual_max_all[0]
    return "Low Max: {:,.0f} km2 - {}".format(low_max, sorted_annual_max_all.index[-1].year)

@app.callback(
    Output('max-diff', 'children'),
    [Input('sea', 'value')])
def current_ice_f(selected_sea):
    year = datetime.now().year
    today_value = df_fdta[selected_sea].iloc[-1]
    current_year_df = df_fdta[selected_sea][df_fdta[selected_sea].index.year == year]
    current_year_max = current_year_df.max()
    change_from_current_year_max = today_value - current_year_max
    return "Change From Max: {:,.0f} km2".format(change_from_current_year_max)

@app.callback(
    Output('daily-low-diff', 'children'),
    [Input('sea', 'value')])
def current_ice_g(selected_sea):
    today_value = df_fdta[selected_sea].iloc[-1]
    dr = df_fdta[(df_fdta.index.month == df_fdta.index[-1].month) & (df_fdta.index.day == df_fdta.index[-1].day)]
    dr_sea = dr[selected_sea]
    sort_dr_sea = dr_sea.sort_values(axis=0, ascending=True)
    daily_low_diff = today_value - sort_dr_sea[0]
    # annual_max_all = df_fdta[selected_sea].loc[df_fdta.groupby(pd.Grouper(freq='Y')).idxmax().iloc[:, 0]]
    # low_max = annual_max_all[0]
    # record_low_max_difference = today_value - low_max
    return "Difference From Date's Low: {:,.0f} km2".format(daily_low_diff)

@app.callback(
    Output('all-ice-extent', 'figure'),
    [Input('sea', 'value')])
def update_figure_a(selected_sea):
    traces = []
    def all_ice_fit():
        xi = arange(0,days)
        slope, intercept, r_value, p_value, std_err = stats.linregress(xi,df[selected_sea])
        return (slope*xi+intercept)
    traces.append(go.Scatter(
        x = df_fdta.index, 
        y = df_fdta[selected_sea],
        name = 'Ice'
    )),
    traces.append(go.Scatter(
        x = df_fdta.index,
        y = all_ice_fit(),
        name = 'trend'
    ))
    return {
        'data': traces,
        'layout': go.Layout(
                xaxis = {'title': ''},
                yaxis = {'title': 'Ice Extent km2'},
                hovermode = 'closest',
                height = 500, 
                title = '{} Ice Extent'.format(selected_sea)
                )  
    }

@app.callback(
    Output('annual-max-table', 'children'),
    [Input('sea', 'value')])
def record_ice_table(selected_sea, max_rows=10):
    annual_max_all = df_fdta[selected_sea].loc[df_fdta.groupby(pd.Grouper(freq='Y')).idxmax().iloc[:, 0]]
    
    sorted_annual_max_all = annual_max_all.sort_values(axis=0, ascending=True)
   
    sama = pd.DataFrame({'Extent km2':sorted_annual_max_all.values,'YEAR':sorted_annual_max_all.index.year})
    sama = sama.round(0)
    return html.Table (
        [html.Tr([
            html.Td(sama.iloc[i].map('{:,.0f}'.format)[0]),
            html.Td(sama.iloc[i][1])
            ]) for i in range(min(len(sama), max_rows))]
    )

@app.callback(
    Output('annual-min-table', 'children'),
    [Input('sea', 'value')])
def record_ice_table_a(selected_sea, max_rows=10):
    annual_min_all = df_fdta[selected_sea].loc[df_fdta.groupby(pd.Grouper(freq='Y')).idxmin().iloc[:, 0]]
    sorted_annual_min_all = annual_min_all.sort_values(axis=0, ascending=True)
    sama = pd.DataFrame({'Extent km2':sorted_annual_min_all.values,'YEAR':sorted_annual_min_all.index.year})
    sama = sama.round(0)
    return html.Table (
        [html.Tr([
            html.Td(sama.iloc[i].map('{:,.0f}'.format)[0]),
            html.Td(sama.iloc[i][1])
            ]) for i in range(min(len(sama), max_rows))]
    )

@app.callback(
    Output('current-date-values', 'children'),
    [Input('sea', 'value')])
def current_date_table(selected_sea, max_rows=10):
    dr = df_fdta[(df_fdta.index.month == df_fdta.index[-1].month) & (df_fdta.index.day == df_fdta.index[-1].day)]
    dr_sea = dr[selected_sea]
    sort_dr_sea = dr_sea.sort_values(axis=0, ascending=True)
  
    sort_dr_sea = pd.DataFrame({'km2':sort_dr_sea.values, 'YEAR':sort_dr_sea.index.year})
    sort_dr_sea= sort_dr_sea.round(0)

    return html.Table (
        [html.Tr([
            html.Td(sort_dr_sea.iloc[i].map('{:,.0f}'.format)[0]), 
            html.Td(sort_dr_sea.iloc[i][1])
        ]) for i in range(min(len(sort_dr_sea), max_rows))]
    )
   
app.layout = html.Div(body)

if __name__ == "__main__":
    app.run_server(port=8124, debug=True)

