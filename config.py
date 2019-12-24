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

# Version "1.1", by Eric, KF7EEL

# Contains all variables and functions for program
# APRS-IS receive script and required by Interactive SMS script. 
# https://github.com/kf7eel/shark-py-sms

# Feel free to modify and improve.


###############################################################################
#CONFIGURATION VARIABLES
###############################################################################

#############################----APRS----######################################
# Callsign and SSID
hotspot_callsign = 'Insert your Callsign'

# APRS-IS passcode
aprs_passcode = 'APRS Passcode'

# Geographical info
latitude = '4726.18N' # Latitude, use this format
longitude = '12019.64W' # Longitude, use this format
altitude = '000679' # Altitude in feet
aprs_comment = 'APRS <-> DMR SMS gateway test'
aprs_beacon_1_comment = 'https://github.com/kf7eel/shark-py-sms'
aprs_beacon_2_comment = 'APRS to DMR SMS demo'
aprs_symbol_table = '/' #Primary table
aprs_symbol = '-' # "House" symbol

# Location packet
#location_packet = hotspot_callsign + '>APRS,TCPIP*:' + '=' + latitude + '/' + longitude + aprs_symbol + aprs_symbol_table + 'A=' + altitude + ' ' + aprs_comment


# Filter to be sent to server, required for incoming packets. 100km radius of Ellensberg, WA
# Must change this to your QTH and change radius.
aprs_filter = 'r/47/-120/100'


# ! - fixed short format, = - message capable,

# Enable logging
#logging.basicConfig(level=logging.DEBUG) # level=10, DEBUG for most info

###########################----DMR SMS----######################################

#--------------------------------------------------------
# User, Password, and smtp server of your email account. 
email_user = 'E-Mail address'                              
email_password = 'E-Mail password'                     
email_server = 'E-Mail server'                             
smtp_port = 465                                          
pop_port = 995                                           
#--------------------------------------------------------

# Override variables, used in reply function to override the default of replying to what was received.
# Use these to specify all replies to a talkgroup for axample. Some radios will not send ACK
# packet in correct time, resulting in a million messages from the modem.
o_sms_type =  "1"
o_sms_format = "2"
o_sms_source = "9"
o_sms_message = None

# Line break variable, used to sort for exact strings. Used variable to mkae code look pretty.
line_break = '\n'
sms_file = '/tmp/.shark.sms'

# Global Variables
sms_type =  None #"1"
sms_format = None #"2"
sms_source = None #"9"
sms_message = None
sms_modem = "1"
data = None

################################################################################
