from ftplib import FTP
import os
import pandas as pd


# Log into ftp site.
ftp = FTP('sidads.colorado.edu')
ftp.login(user='anonymous', passwd='ICE_PSWD')
ftp.login()
# Read file.
ftp.cwd('/pub/DATASETS/NOAA/G02135/north/daily/data/')
ftp.retrbinary('RETR N_seaice_extent_daily_v3.0.csv', open('N_seaice_extent_daily_v3.0.csv', 'wb').write)
ftp.quit()

# Read data.
df = pd.read_csv('N_seaice_extent_daily_v3.0.csv',skiprows=[i for i in range(1,2436)])
# df.columns =  []

pd.options.display.float_format = '{:,}'.format



print(df.head())