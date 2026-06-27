
# import datetime
import datetime as dt

d1=dt.datetime(2026,6,27,16,15,15)
print(d1)
print(d1.weekday())
print(d1.date())
print(d1.time())
# import datetime

# d1=datetime.datetime(2026,6,27)
# print(d1)

d0=dt.date(2026,6,27)
print(d0)
t1=dt.time(16,15,15)
print(t1)


delta1=dt.timedelta(minutes=5)
print(d1+delta1)