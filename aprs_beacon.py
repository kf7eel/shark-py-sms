#!/usr/bin/python3.7

###############################################################################
#   Copyright (C) 2019 Eric Craw, KF7EEL <kf7eel@qsl.net>
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software Foundation,
#   Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301  USA
###############################################################################

# Version "1.0", by Eric, KF7EEL

# Timed APRS beacon script. 
# https://github.com/kf7eel/shark-py-sms

# Feel free to modify and improve.

from functions_v1 import *

beacon_time = 900 # Time in seconds, 15 minutes

def beacon_loop():
    while 1 < 5:
        aprs_location()
        time.sleep(beacon_time) #15 minutes
        aprs_beacon_1()
        time.sleep(beacon_time) #15 minutes
        aprs_beacon_2()
        time.sleep(beacon_time) #15 minutes
   

# Connect ot APRS-IS
AIS.connect()

aprs_beacon_1()


# Statr loop with exception handle

n = 2
iarl = 1
while iarl < n:
    try:
        print('Initialize')
        beacon_loop()
        iarl += 1
    except:
        print('exception, reset')
        time.sleep(2)
        AIS.connect()
        time.sleep(2)
        beacon_loop()
        iarl = 2
    finally:
        print('exception final, reset')
        time.sleep(2)
        AIS.connect()
        time.sleep(2)
        beacon_loop()
        iarl = 2        

    
