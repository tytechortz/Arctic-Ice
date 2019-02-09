import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import sqlite3
from dash.dependencies import Input, Output
import datetime as dt 
import dash_table

app = dash.Dash(__name__)


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


annual_maximums = df2[' (0) Northern_Hemisphere'].loc[df2.groupby(pd.Grouper(freq='Y')).idxmax().iloc[:-1, 0]]
print(annual_maximums)


app.layout = html.Div([
    html.Div(
        className="app-header",
        children=[
            html.Div('Arctic Sea Ice Extent', className="app-header--title"),
        ]
    ),
    html.Div(
        children=html.Div(
             html.H3(children='1988-Present'),
        )
    ),
    html.Div(
        children=html.Div(
             html.H3(children='Data From National Snow and Ice Data Center'),
        )
    ),
    dcc.Graph(
        id='ice-extent'),
        html.Div([
            dcc.RangeSlider(
                id='ice-slider',
                min=value_range[0],
                max=value_range[1],
                step=1,
                value=[0, 365],
                # marks={i: i for i in range(value_range[0], value_range[1]+ 1)}
            ),
            html.Div([
            html.H2('Slider to Select Day Range')
        ]),
        ]),
        html.Div([
            html.H2('Select Years'),
        ]),
        html.Div([
            html.Div([
                dcc.Dropdown(
                id='year1',
                options=year_options,
                value="2007"),
            ],
            style={'width': '20%', 'display': 'inline-block'}),
            html.Div([
                dcc.Dropdown(
                id='year2',
                options=year_options,
                value="2012"),
            ],
            style={'width': '20%', 'display': 'inline-block'}),
            html.Div([
                dcc.Dropdown(
                id='year3',
                options=year_options,
                value="2016"),
            ],
            style={'width': '20%', 'display': 'inline-block'}),
            html.Div([
                dcc.Dropdown(
                id='year4',
                options=year_options,
                value="2018"),
            ],
            style={'width': '20%', 'float': 'right', 'display': 'inline-block'}),
            html.Div([
                dcc.Dropdown(
                id='year5',
                options=year_options,

                value="2019"),
            ],
            style={'width': '20%', 'float': 'right', 'display': 'inline-block'}),       
            ]),

    html.Div([
            html.H2("Today's Value: {:,.1f} km2".format(today_value)),
        ]),

     html.Div([
            html.H2("24 Hour Change: {:,.1f} km2".format(daily_difference)),
        ]),   

    html.Div([
            html.H2('Record Minimum: {:,.1f} km2'.format(record_low[0])),
        ]),
    html.Div([
            html.H2('Difference From Minimum: {:,.1f} km2'.format(record_low_difference)),
        ]),  
    html.Ul([html.Li(x) for x in annual_maximums])   
])



@app.callback(
    Output('ice-extent', 'figure'),
    [Input('year1', 'value'),
    Input('year2', 'value'),
    Input('year3', 'value'),
    Input('year4', 'value'),
    Input('year5', 'value'),
    Input('ice-slider', 'value')])
def update_figure(selected_year1,selected_year2,selected_year3,selected_year4,selected_year5, value_range):
    traces = []
    selected_years = [selected_year1,selected_year2,selected_year3,selected_year4,selected_year5]
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
                height = 800,
                title = 'Arctic Sea Ice Extent',
                xaxis = {'title': 'Day', 'range': value_range},
                yaxis = {'title': 'Ice extent (km2)'},
                hovermode='closest',
                )  
    }

if __name__ == '__main__':
    app.run_server(port=8124)   