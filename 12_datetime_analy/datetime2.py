

data1='2026-06-27'
#str to datetime


import datetime as dt
dt1=dt.datetime.strptime(data1,'%Y-%m-%d')
print(dt1)

date2='Dec 29, 2026'
f='%b %d, %Y'
dt2=dt.datetime.strptime(date2,f)
print(dt2)

data3='12/29/2026'
f1='%m/%d/%Y'
dt3=dt.datetime.strptime(data3,f1)
print(dt3)

#epoch time
#1971

n1=1782562387+60
dt4=dt.datetime.fromtimestamp(n1)
print(dt4)

e1=dt4.timestamp()
print(e1)

current_time=dt.datetime.now()
print(current_time)
print(current_time.timestamp())