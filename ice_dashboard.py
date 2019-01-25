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

years = df.columns 


app.layout = html.Div([
    dcc.Graph(id='ice-extent'),

    html.Div([
        dcc.Dropdown(
            id='xaxis',
            options=[{'label': i, 'value': i} for i in years],
            placeholder='select years',
            # multi=True
            # value='#num'
        )
    ]),

    html.Div([
        dcc.RadioItems(
            id='decade',
            options=[
                {'label': "1980's Avg", 'value': "1980's Average"},
                {'label': "1990's Avg", 'value': "1990's Average"},
                {'label': "2000's Avg", 'value': "2000's Average"},
                {'label': "2010's Avg", 'value': "2010's Average"},
                ],
        )
    ]),
])

@app.callback(
    Output('ice-extent', 'figure'),
    [Input('xaxis', 'value'),
    Input('decade', 'value')])
def update_graph(xaxis_name, decade):
    traces = []
    traces.append(go.Scatter(
        x=df['#num'],
        y=df[xaxis_name],
        mode='markers', 
    ))
    traces.append(go.Scatter(
        x=df['#num'],
        y=df[decade],
        mode='markers',
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
