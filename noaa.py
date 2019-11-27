#!/usr/bin/python

# Script created by Eric - KF7EEL

# This script will check for the specified alert types, then send
# SMS to the configured DMR ID or Talk group.
# Configure group of same codes to receive alerts for thos counties.
# Set this on a cron job to check regularly.

import re, binascii, shark, time
from weatheralerts import WeatherAlerts

# Configure SMS here.
# sms_type, 0 = private, 1 = group
# sms_format, 0 = ETSI, 1 = UDP, 2 = UDP/Chinese
# sms_dest, Talk group or DMR ID
# sms_modem, 0 = Network, send SMS to the network, 1 = Modem, send SMS to modem only,
# will not get sent to network

sms_type = "1"
sms_format = "2"
sms_dest = "9"
sms_modem = "1"

shark.do_checkauth()

# Same codes for Chelan, Douglas, Grant, and Okanogan Counties
nws = WeatherAlerts(samecodes=['053007','053017','053025','053047'])

# Same codes for entire state
#nws = WeatherAlerts(state='WA')

# Filter for Severe alerts
for alert in nws.alerts:
    if "Severe" in alert.severity:
# 1=Type, Group | 2=Format, UDP/Chinese | 9=Talkgroup | alert.title= message
        shark.do_send_sms(sms_type, sms_format, sms_dest, sms_modem, alert.title)
        print(alert.title)
        print(alert.severity)
        print(alert.urgency)
        print(alert.areadesc)
        print(alert.samecodes)
        print(alert.expiration)
        print("\n")
        time.sleep(1)

# Filter for Moderate alerts
    if "Moderate" in alert.severity:
        shark.do_send_sms(sms_type, sms_format, sms_dest, sms_modem, alert.title)
        print (alert.title)
        print (alert.severity)
        print(alert.urgency)
        print(alert.areadesc)
        print(alert.samecodes)
        print(alert.expiration)
        print("\n")
        time.sleep(1)

# Filter for Extreme alerts
    if "Extreme" in alert.severity:
        shark.do_send_sms(sms_type, sms_format, sms_dest, sms_modem, alert.title)
        print (alert.title)
        print (alert.severity)
        print(alert.urgency)
        print(alert.areadesc)
        print(alert.samecodes)
        print(alert.expiration)
        print("\n")
        time.sleep(1)

