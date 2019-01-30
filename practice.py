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

app.layout = html.Div([
    dcc.Graph(id='ice-extent'),
        html.Div([
            html.Div([
                dcc.Dropdown(
                id='year1',
                options=[{'label': i, 'value': i} for i in years],
                placeholder='select years',
                value="2019")
            ]),
            html.Div([
                dcc.Dropdown(
                id='year2',
                options=[{'label': i, 'value': i} for i in years],
                placeholder='select years',
                value="2019")
            ]),
        ])

    
])

@app.callback(
    Output('ice-extent', 'figure'),
    [Input('year1', 'value'),
    Input('year2', 'value')])
def update_graph(selected_year1, selected_year2):
    traces = []
    # df_new = df[df[selected_year1] == selected_year1]
    for years in df:
        traces.append(go.Scatter(
            x=df['#num'],
            y=df[selected_year1],
            mode='lines',
        ))
    for years in df:
        traces.append(go.Scatter(
            x=df['#num'],
            y=df[selected_year2],
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