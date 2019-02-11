import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import sqlite3
from dash.dependencies import Input, Output
import datetime as dt 
import dash_table


df2=pd.read_csv('ftp://sidads.colorado.edu/DATASETS/NOAA/G02186/masie_4km_allyears_extent_sqkm.csv', skiprows=1)
df2['yyyyddd'] = pd.to_datetime(df2['yyyyddd'], format='%Y%j')
df2.set_index('yyyyddd', inplace=True)




df3 = df2[' (0) Northern_Hemisphere'].loc[df2.groupby(pd.Grouper(freq='Y')).idxmax().iloc[:-1, 0]]
print(df3.sort_values(axis=0, ascending=False))
sms = df3.sort_values(axis=0, ascending=False)

print(sms)

# app = dash.Dash(__name__)

# app.layout = html.Div([
#      html.Ol(
#         html.Li(df2(index, value))
#     ),
# ])



    

# if __name__ == '__main__':
#     app.run_server(debug=True, threaded=True,port=8124)