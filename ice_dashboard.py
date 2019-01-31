import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import sqlite3
from dash.dependencies import Input, Output

# database connection
cnx = sqlite3.connect('sea-ice.db')

# Launch the application:
app = dash.Dash()

# Create a DataFrame from the .csv file:
df = pd.read_sql_query("SELECT * FROM ice", cnx)
# df = pd.read_csv('./sea_ice.csv')

years = df.columns[4:]

value_range = [0, 365]

app.layout = html.Div([
    html.H1(children='Arctic Sea Ice Extent'),
    html.H4(children='1978-Present with Decade Averages'),
    dcc.Graph(id='ice-extent'),
        html.Div([
            html.H2('Slider to Select Day Range')
        ]),
        html.Div([
            dcc.RangeSlider(
                id='ice-slider',
                min=value_range[0],
                max=value_range[1],
                step=1,
                value=[0, 365],
                # marks={i: i for i in range(value_range[0], value_range[1]+ 1)}
            ),
        ]),
        html.Div([
            html.H2('Select Years'),
        ]),
        html.Div([
            html.Div([
                dcc.Dropdown(
                id='year1',
                options=[{'label': i, 'value': i} for i in years],
                placeholder='select years',
                value="2018"),
            ],
            style={'width': '48%', 'display': 'inline-block'}),
            html.Div([
                dcc.Dropdown(
                id='year2',
                options=[{'label': i, 'value': i} for i in years],
                placeholder='select years',
                value="2019"),
            ],
            style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),       
            ]),
])

@app.callback(
    Output('ice-extent', 'figure'),
    [Input('year1', 'value'),
    Input('year2', 'value'),
    Input('ice-slider', 'value')])
def update_graph(selected_year1, selected_year2, value_range):
    traces = []
    traces.append(go.Scatter(
            x=df['#num'],
            y=df[selected_year1],
            mode='lines',
            name=selected_year1
        ))
    traces.append(go.Scatter(
            x=df['#num'],
            y=df[selected_year2],
            mode='lines',
            name=selected_year2
        ))
    return {
        'data': traces,
        'layout': go.Layout(
                title = 'Arctic Sea Ice Extent',
                xaxis = {'range': value_range, 'title': 'Day'},
                yaxis = {'title': 'Ice extent (km2)'},
                hovermode='closest',
                )  
    }


    
# Add the server clause:
if __name__ == '__main__':
    app.run_server()