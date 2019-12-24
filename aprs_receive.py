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

# Interactive APRS script. 
# https://github.com/kf7eel/shark-py-sms

# Feel free to modify and improve.
from functions_v1 import *

global AIS

AIS = aprslib.IS(hotspot_callsign, passwd=aprs_passcode, port=14580)
#print(hotspot_callsign + '>APRS,TCPIP*:' + '=' + latitude + '/' + longitude + '</A' + altitude + ' ' + aprs_comment)

AIS.set_filter(aprs_filter)
AIS.connect()

#print(location_packet)
#AIS.sendall(location_packet)

n = 2
iarl = 1
while iarl < n:
    
    try:
        print('Initialize')
        AIS.consumer(aprs_receive_loop, raw=True)
        iarl += 1
    except:
        print('Exception, reseting')
        AIS.connect()
        AIS.consumer(aprs_receive_loop, raw=True)
        iarl = 2
    finally:
        print('Exception, finally, restarting')
        AIS.connect()
        AIS.consumer(aprs_receive_loop, raw=True)
        iarl = 2

