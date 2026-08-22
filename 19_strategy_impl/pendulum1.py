

time_frame1=10

import datetime as dt


time_zone1= 'America/New_York'
time_zone2= 'Asia/Kolkata'

import pendulum as pdlm
print(dt.datetime.now())
print(pdlm.now(tz=time_zone1))
print(pdlm.now(tz=time_zone2))
