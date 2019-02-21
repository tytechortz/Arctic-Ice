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
df3 = df2[' (0) Northern_Hemisphere'].loc[df2.groupby(pd.Grouper(freq='Y')).idxmax().iloc[:, 0]]
df4 = df3.sort_values(axis=0, ascending=False)
df_min = df2[' (0) Northern_Hemisphere'].loc[df2.groupby(pd.Grouper(freq='Y')).idxmin().iloc[:, 0]]
df5 = df_min.sort_values(axis=0, ascending=False)

df_min_max = df3[0]
record_low_max_difference = today_value - df_min_max


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
                style={'height':40, 'align':'start'} 
            ),
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
                     html.H2("24 Hour Change: {:,.1f} km2".format(daily_difference)),
                ]),
                style={'height':40, 'align':'end'} 
            ),
            dbc.Col(
                html.Div([
                    html.H2('Difference: {:,.1f} km2'.format(record_min_difference)),
                ]),
                style={'height':40, 'align':'start'} 
            ), 
        ]),
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.H2('Record Maximum: {:,.1f} km2, {}'.format(record_max[0], df4.index[0].year)),
                ]),
                style={'height':40, 'align':'end'} 
            ),
            dbc.Col(
                html.Div([
                    html.H2('Record Low Maximum: {:,.1f} km2, {}'.format(df_min_max, df3.index[0].year)),
                ]),
                style={'height':40, 'align':'start'} 
            ),  
        ]),
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.H2('Difference: {:,.1f} km2'.format(record_max_difference)),
                ]),
                style={'height':40, 'align':'start'} 
            ),
            dbc.Col(
                html.Div([
                    html.H2('Difference: {:,.1f} km2'.format(record_low_max_difference)),
                ]),
                style={'height':40, 'align':'start'} 
            ), 
        ]),
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.H2('Annual Low Maximum Rankings',style={'color': 'black','font-size':40}),
                ]),
                style={'height':40, 'align':'start'} 
            ),
            dbc.Col(
                html.Div([
                    html.H2('Annual Minimum Rankings',style={'color': 'black','font-size':40}),
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
            ) 
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