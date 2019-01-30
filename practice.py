import plotly.plotly as py
import plotly.graph_objs as go
import sqlite3
import pandas as pd 

cnx = sqlite3.connect('sea-ice.db')

df = pd.read_sql_query("SELECT * FROM ice", cnx)

print(df).head()