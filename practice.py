import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import sqlite3
from dash.dependencies import Input, Output
import datetime as dt 

df=pd.read_csv('ftp://sidads.colorado.edu/DATASETS/NOAA/G02186/masie_4km_allyears_extent_sqkm.csv', skiprows=1)
df['yyyyddd'] = pd.to_datetime(df['yyyyddd'], format='%Y%j')
df.set_index('yyyyddd', inplace=True)

print(df.head())

annual_maximums = df[' (0) Northern_Hemisphere'].loc[df.groupby(pd.Grouper(freq='Y')).idxmax().iloc[:-1, 0]]
print(annual_maximums)



    
# Add the server clause:
# if __name__ == '__main__':
#     app.run_server()