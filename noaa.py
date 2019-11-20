#!/usr/bin/python
import re, binascii, shark
from weatheralerts import WeatherAlerts

alert_msg = '/tmp/.shark.alert_msg'
f = open(alert_msg)
lines = f.read() # lines()


nws = WeatherAlerts(samecodes=['015001']) #,'015003'])
for alert in nws.alerts:
#    if "Severe" or "Extreme" in alert.severity:
    f_alert = open(alert_msg, 'w')
    f_alert.write(alert.title)
    f_alert.close
# 1=Type, Group | 2=Format, UDP/Chinese | 9=Talkgroup | alert.title= message
    shark.do_send_sms('1', '2', '9', alert.title)
    print(alert.title)
    print(alert.severity)
