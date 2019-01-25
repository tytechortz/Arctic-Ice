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
    html.Div([
        dcc.Dropdown(
            id='xaxis',
            options=[{'label': i, 'value': i} for i in years],
            value='displacement'
        )
    ],
    
    )
])

# Add the server clause:
if __name__ == '__main__':
    app.run_server()
