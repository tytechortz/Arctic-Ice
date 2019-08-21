from ftplib import FTP

ftp = FTP('sidads.colorado.edu')
# ftp = FTP('ftp.cse.buffalo.edu')
ftp.login(user='anonymous', passwd='')
# ftp.login()

print(ftp.login())


