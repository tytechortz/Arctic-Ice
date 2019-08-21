from ftplib import FTP
import os
import pandas as pd

ftp = FTP('sidads.colorado.edu')
# ftp = FTP('ftp.cse.buffalo.edu')
ftp.login(user='anonymous', passwd='ICE_PSWD')
# ftp.login()

print(ftp.login())

ftp.cwd('/pub/DATASETS/NOAA/G02135/north/daily/data/')
files = ftp.dir()
ftp.retrbinary('RETR N_seaice_extent_daily_v3.0.csv', open('N_seaice_extent_daily_v3.0.csv', 'wb').write)
ftp.quit()

df = pd.read_csv('N_seaice_extent_daily_v3.0.csv')

print(df.head())