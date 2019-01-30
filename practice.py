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

years = df.columns[4:]

app.layout = html.Div([
    dcc.Graph(id='ice-extent'),
        html.Div([
            html.Div([
                dcc.Dropdown(
                id='year1',
                options=[{'label': i, 'value': i} for i in years],
                placeholder='select years'),
                # value='#num'
            ]),
            html.Div([
                dcc.Dropdown(
                id='year2',
                options=[{'label': i, 'value': i} for i in years],
                placeholder='select years'),
            ]),
        ])

    
])

@app.callback(
    Output('ice-extent', 'figure'),
    [Input('year1', 'value'),
    Input('year2', 'value')])
def update_graph(year1, year2):
    traces = []
    for year1 in df:
        traces.append(go.Scatter(
            x=df['#num'],
            y=df[year1],
            mode='lines',
        ))
    for year2 in df:
        traces.append(go.Scatter(
            x=df['#num'],
            y=df[year2],
            mode='lines',
        ))
    return {
        'data': traces,
        'layout': go.Layout(
                title = 'Arctic Sea Ice Extent',
                xaxis = {'title': 'Day'},
                yaxis = {'title': 'Ice extent (km2)'},
                hovermode='closest'
        )
    }

    
# Add the server clause:
if __name__ == '__main__':
    app.run_server()