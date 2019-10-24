import psycopg2
import pandas as pd
import time
import requests
import sqlalchemy

today = time.strftime("%Y-%m-%d")

df = pd.read_csv('./cleaned_masie.csv', skiprows=1)

# df = pd.read_csv('https://www.ncei.noaa.gov/access/services/data/v1?dataset=daily-summaries&dataTypes=TMAX,TMIN&stations=USW00023062&startDate=1950-01-01&endDate=' + today + '&units=standard').round(1)
df['yyyyddd'] = pd.to_datetime(df['yyyyddd'], format='%Y%j')
df.set_index('yyyyddd', inplace=True)
df.columns = ['Total Arctic Sea', 'Beaufort Sea', 'Chukchi Sea', 'East Siberian Sea', 'Laptev Sea', 'Kara Sea',\
     'Barents Sea', 'Greenland Sea', 'Bafin Bay Gulf of St. Lawrence', 'Canadian Archipelago', 'Hudson Bay', 'Central Arctic',\
         'Bering Sea', 'Baltic Sea', 'Sea of Okhotsk', 'Yellow Sea', 'Cook Inlet']

print(df)
# engine = sqlalchemy.create_engine("postgresql://postgres:1234@localhost/denver_temps")
# con = engine.connect()

# print(engine.table_names())

# table_name = 'temps'
# df.to_sql(table_name, con)
# print(engine.table_names())

# con.close()