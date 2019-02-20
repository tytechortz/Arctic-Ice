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
df['datetime']= pd.to_datetime(df['yyyyddd'])
df = df.set_index('datetime')


value_range = [0, 365]

year_options = []
# for YEAR in df['yyyyddd'].dt.strftime('%Y').unique():
for YEAR in df.index.year.unique():
    year_options.append({'label':(YEAR), 'value':YEAR})

# df2=df[(df['yyyyddd'].dt.year == 2017)]


today_value = df[' (0) Northern_Hemisphere'].iloc[-1]
daily_difference = df[' (0) Northern_Hemisphere'].iloc[-1] - df[' (0) Northern_Hemisphere'].iloc[-2]
record_min = df[' (0) Northern_Hemisphere'].min(),
df[' (0) Northern_Hemisphere'].iloc[-1]
record_min_difference = today_value - record_min[0]
record_max = df[' (0) Northern_Hemisphere'].max(),
record_max_difference = today_value - record_max[0]


df2=pd.read_csv('ftp://sidads.colorado.edu/DATASETS/NOAA/G02186/masie_4km_allyears_extent_sqkm.csv', skiprows=1)
df2['yyyyddd'] = pd.to_datetime(df2['yyyyddd'], format='%Y%j')
df2.set_index('yyyyddd', inplace=True)
df3 = df2[' (0) Northern_Hemisphere'].loc[df2.groupby(pd.Grouper(freq='Y')).idxmax().iloc[:-1, 0]]
df4 = df3.sort_values(axis=0, ascending=False)


df_min_max = df3[0]


annual_maximums = df2[' (0) Northern_Hemisphere'].loc[df2.groupby(pd.Grouper(freq='Y')).idxmax().iloc[:-1, 0]]


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
                    html.H3('2008-Present', style={'text-align': 'center'}),
                ),
                width={'size': 6, 'offset': 3}
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
                    html.H2('Select Years', style={'text-align': 'center'}),
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
                style={'height':40, 'align':'start'} 
            ), 
        ]),
        dbc.Row([
            dbc.Col(
                html.Div([
                     html.H2("24 Hour Change: {:,.1f} km2".format(daily_difference)),
                ]),
                style={'height':40, 'align':'end'} 
            ), 
        ]),
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.H2('Record Minimum: {:,.1f} km2'.format(record_min[0])),
                ]),
                style={'height':40, 'align':'end'} 
            ), 
        ]),
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.H2('Difference From Minimum: {:,.1f} km2'.format(record_min_difference)),
                ]),
                style={'height':40, 'align':'start'} 
            ), 
        ]),
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.H2('Record Maximum: {:,.1f} km2'.format(record_max[0])),
                ]),
                style={'height':40, 'align':'end'} 
            ), 
        ]),
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.H2('Difference From Maximum: {:,.1f} km2'.format(record_max_difference)),
                ]),
                style={'height':40, 'align':'start'} 
            ), 
        ]),
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.H2('Record Low Maximum: {:,.1f} km2'.format(df_min_max)),
                ]),
                style={'height':40, 'align':'start'} 
            ), 
        ]),
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.H2('Annual Maximum Rankings'),
                ]),
                style={'height':40, 'align':'start'} 
            ),
            dbc.Col(
                html.Div([
                    html.H2("1- {:,.1f} km2".format(df4[12])),
                ]),
                style={'height':40, 'align':'start'} 
            ), 
        ]),
        
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