import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import sqlite3

# database connection
cnx = sqlite3.connect('sea-ice.db')

# Launch the application:
app = dash.Dash()

# Create a DataFrame from the .csv file:
df = pd.read_sql_query("SELECT * FROM ice", cnx)

# year_options = []
# for column in df

# Create a Dash layout that contains a Graph component:
app.layout = html.Div([

    html.Div([
        dcc.Graph(
            id='ice_extent',
            figure={
                'data': [
                    go.Scatter(
                        x = df["#num"],
                        y = df["2010's Average"],
                        mode = 'markers'
                    )
                ],
                'layout': go.Layout(
                    title = 'Arctic Sea Ice Extent',
                    xaxis = {'title': 'Day'},
                    yaxis = {'title': 'Ice extent (km2)'},
                    hovermode='closest'
                )
            }
        ),
        dcc.Dropdown(
            id='xaxis',
            options=[{'label': i, 'value': i} for i in df.columns],
            value='Loc',
            placeholder="Select Data"
        )
    ])
])

# Add the server clause:
if __name__ == '__main__':
    app.run_server()
