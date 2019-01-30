# Perform imports here:
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import sqlite3

# Launch the application:
app = dash.Dash()

cnx = sqlite3.connect('sea-ice.db')

df = pd.read_sql_query("SELECT * FROM ice", cnx)

years = df.columns



# Create a Dash layout that contains a Graph component:
app.layout = html.Div([
    dcc.Graph(
        id='ice',
        figure={
            'data': [
                go.Scatter(
                    x = df['#num'],
                    y = df['2000'],
                    mode = 'markers'
                )
            ],
            'layout': go.Layout(
                title = 'Arctic Sea Ice Extent',
                xaxis = {'title': 'Day'},
                yaxis = {'title': 'Ice Extent in km2'},
                hovermode='closest'
            )
        }
    )
])

# Add the server clause:
if __name__ == '__main__':
    app.run_server()