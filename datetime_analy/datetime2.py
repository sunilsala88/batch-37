

data1='2026-06-27'
#str to datetime


import datetime as dt
dt1=dt.datetime.strptime(data1,'%Y-%m-%d')
print(dt1)

date2='Dec 29, 2026'
f='%b %d, %Y'
dt2=dt.datetime.strptime(date2,f)
print(dt2)

