# Perform imports here:
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import sqlite3
from dash.dependencies import Input, Output

# Launch the application:
app = dash.Dash()

cnx = sqlite3.connect('sea-ice.db')

df = pd.read_sql_query("SELECT * FROM ice", cnx)

years = df.columns


app.layout = html.Div([
    dcc.Graph(id='ice-extent'),

    html.Div([
        dcc.Dropdown(
            id='xaxis',
            options=[{'label': i, 'value': i} for i in years],
            placeholder='select years'
        )
    ])
])


@app.callback(
    Output('ice-extent', 'figure'),
    [Input('xaxis', 'value')])
def update_graph(xaxis_name):
    return{
        'data': [
            go.Scatter(
                x = df['#num'],
                y = df['2000'],
                mode='markers',
        )],
        'layout': go.Layout(
                title = 'Arctic Sea Ice Extent',
                xaxis = {'title': 'Day'},
                yaxis = {'title': 'Ice Extent in km2'},
                hovermode='closest'
            )
    }

# app.layout = html.Div([
#     dcc.Graph(
#         id='ice',
#         figure={
#             'data': [
#                 go.Scatter(
#                     x = df['#num'],
#                     y = df['2000'],
#                     mode = 'markers'
#                 )
#             ],
#             'layout': go.Layout(
#                 title = 'Arctic Sea Ice Extent',
#                 xaxis = {'title': 'Day'},
#                 yaxis = {'title': 'Ice Extent in km2'},
#                 hovermode='closest'
#             )
#         }
#     )
# ])

# Add the server clause:
if __name__ == '__main__':
    app.run_server()