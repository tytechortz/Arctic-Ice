import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import sqlite3
from dash.dependencies import Input, Output
import datetime as dt 

app = dash.Dash(__name__)



df = pd.read_csv('ftp://sidads.colorado.edu/DATASETS/NOAA/G02186/masie_4km_allyears_extent_sqkm.csv', skiprows=1)

df['yyyyddd'] = pd.to_datetime(df['yyyyddd'], format='%Y%j')

value_range = [0, 365]

year_options = []
for YEAR in df['yyyyddd'].dt.strftime('%Y').unique():
    year_options.append({'label':(YEAR), 'value':YEAR})


app.layout = html.Div([
    html.Div(
        className="app-header",
        children=[
            html.Div('Arctic Sea Ice Extent', className="app-header--title"),
        ]
    ),
    html.Div(
        children=html.Div(
             html.H3(children='1988-Present')
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
                options=[year_options],
                placeholder='select years',
                value="2007"),
            ],
            style={'width': '20%', 'display': 'inline-block'}),
            html.Div([
                dcc.Dropdown(
                id='year2',
                options=[year_options],
                placeholder='select years',
                value="2012"),
            ],
            style={'width': '20%', 'display': 'inline-block'}),
            html.Div([
                dcc.Dropdown(
                id='year3',
                options=[year_options],
                placeholder='select years',
                value="2016"),
            ],
            style={'width': '20%', 'display': 'inline-block'}),
            html.Div([
                dcc.Dropdown(
                id='year4',
                options=[year_options],
                placeholder='select years',
                value="2018"),
            ],
            style={'width': '20%', 'float': 'right', 'display': 'inline-block'}),
            html.Div([
                dcc.Dropdown(
                id='year5',
                options=[year_options],
                placeholder='select years',
                value="2019"),
            ],
            style={'width': '20%', 'float': 'right', 'display': 'inline-block'}),       
            ]),

        html.Div([
            html.H2('Select Decade Average'),
        ]),
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
    print(selected_years)
    # int(selected_year1)
    # print(type(selected_year1))
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
    app.run_server()   