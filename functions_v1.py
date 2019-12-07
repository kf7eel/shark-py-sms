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

# Import modules
# DMR SMS
import re, binascii, shark, time, os, datetime, smtplib
import email, poplib
from email.header import decode_header
# APRS
import aprslib, logging

########################----DMR SMS Functions---#################################

def sms_get():
    #print("Checking for authorization...")
    #shark.do_checkauth()
    print("Fetching SMS")
    shark.do_recieve_sms()


def sms_read():
    global sms_type, sms_format, sms_source, sms_message, sms_modem
    with open(sms_file) as data_file:
        data=data_file.readlines()
        sms_type = data[0]
        sms_format = data[1]
        sms_source = data[2]
        sms_message = data[3]
        if sms_message == '\n':
            print("No SMS messages")
        else:
            print('\n')
            print("Message Received")
            print('\n' + "--------------------------------------" + '\n')
            print("Call Type: " + sms_type)
            print("Format: " + sms_format)
            print("From: " + sms_source)
            print("Message: " + sms_message)
            print('\n' + "--------------------------------------" + '\n')


def reply_sms(message):
    global sms_type, sms_format, sms_source, sms_message, sms_modem
    print('\n')
    print("Sending SMS reply...")
    print('\n')
    time.sleep(2)
    #shark.do_send_sms(sms_type, sms_format, sms_source, sms_modem, message)
    # For testing purposes, below is set to group SMS due to issues with AT-D878. o_ indicates override, see above
    shark.do_send_sms(o_sms_type, o_sms_format, o_sms_source, sms_modem, message)
    print("SMS type: " + sms_type)
    print("Format: " + sms_format)
    print("Source: " + sms_source)
    print("Message: " + message)
        


def email_send(to_email, email_body):
    sent_from = email_user
    to = [to_email]
    subject = 'DMR SMS from ' + str(sms_source)
    body = str(email_body)

    email_text = """\
From: %s
To: %s
Subject: %s

%s
""" % (sent_from, ", ".join(to), subject, body)

    try:
        server = smtplib.SMTP_SSL(email_server, smtp_port)
        server.ehlo()
        server.login(email_user, email_password)
        server.sendmail(sent_from, to, email_text)
        server.close()
        reply_sms('E-Mail sent to ' + to_email)
    except:
        print('Sending email failed')
        reply_sms('Sending Failed')


# Email Receive function, heavily modified code from examples https://www.informit.com/articles/article.aspx?p=686162&seqNum=6
# and https://stackoverflow.com/questions/2260316/deleting-the-most-recently-received-email-via-python-script
def get_email():
    # Use e-mail variables from above
    pop_server = poplib.POP3_SSL(email_server, pop_port)
    pop_server.user(email_user)
    pop_server.pass_(email_password)

# Get the number of mail messages
    numMessages = len(pop_server.list()[1])

# print
    print("E-Mail messages received:")

#List the subject line of each message, then sort for "TO-", where DMR ID is extracted
    for mList in range(numMessages) :
        # Used to number messages with "TO-" in subject, for deletion later
        del_msg = mList + 1
        # Actually filter by subject
        for rec_email_msg in pop_server.retr(mList+1)[1]:
            if rec_email_msg.startswith(b'Subject: TO-'):
                string_email_message = rec_email_msg.decode('utf-8')
                for iem in string_email_message.split():
                    if iem.startswith('TO-'):
                        # Get DMR ID
                        dmr_dst = iem.replace('TO-', '')
                        # Form SMS message, presently includes destination DMR ID, will fix later
                        dmr_email_msg = string_email_message.replace('Subject: TO-', '')
                        print('Destination: ' + dmr_dst)
                        print('Message: ' + dmr_email_msg)
                        print('\n')
                        print('Sending messages via SMS...')
                        shark.do_send_sms(o_sms_type, o_sms_format, o_sms_source, sms_modem, dmr_email_msg)
                        print('Deleting message')
                        pop_server.dele(del_msg)
                        #break
    pop_server.quit()

def main():
    global data, sms_type, sms_format, sms_source, sms_message, sms_modem
    # Commands are here
    # line_break vairable used due to how string processed in python, defined above
# Returns uptime of host    
    if 'UPTIME' + line_break == sms_message:
            print('Getting uptime...')
            uptime = os.popen('uptime').read()
            reply_sms(str(uptime))
# Replies the SMS sent anytime ECHO is in SMS
    if 'ECHO' in sms_message:
            reply_sms(sms_message)
            print("Echoing SMS")
# Returns time and date of host, in UTC?
    if 'TIME' + line_break == sms_message:
            print('Getting time...')
            current_time = time.strftime('%H:%M %A %B %d, %Y - Timezone: %z')
            reply_sms(current_time)
    if 'PING' + line_break == sms_message:
        print("Received ping...")
        time.sleep(0.5)
        print("Pong")
        reply_sms('Pong '+time.strftime('%H:%M:%S - %m/%d/%Y'))
    if 'ID' + line_break == sms_message:
        print('DMR ID: '+ sms_source)
        reply_sms('Your DMR ID is ' + sms_source)
    if 'HELP' + line_break == sms_message:
        print('\n' + "--------------------------------------" + '\n')
        print('Here are the available commands: ')
        print('\n')
        print('HELP - prints current message')
        print('ECHO - replies eniter message back to user')
        print('TIME - current local time')
        print('UPTIME - uptime of host system')
        print('PING - replies with pong')
        print('ID - returns your DMR ID')
        print('If "TO-" and "@" are in message, will send email to address.')
        print('\n' + "--------------------------------------" + '\n')
        reply_sms('1 of 4. All commands are in CAPS. ECHO - replies entier message back to user.')
        reply_sms('2 of 4. TIME - current local time. UPTIME - uptime of host system.')
        reply_sms('3 of 4. PING - replies with pong. ID - returns your DMR ID.')
        reply_sms(' 4 of 4. If "TO-" and "@" are in message, will send email to address')

# Sends email via configured SMTP server, SMS must begin with "TO-" and have email address
# attached with no space. The rest of the message is sent in the email body.
# (example "TO-user@example.org This is a test." will result in an email to user@example.org containing
# "TO-user@example.org This is a test." in the body.

    # Filter "TO-" out of message
    if 'TO-' in sms_message:
        # Filter @ out os SMS, creat another if statement at this level for APRS implimentation.
        if '@' in sms_message:
                print("Perparing email...")
                for i in sms_message.split():
                    if i.startswith("TO-"):
                        #print(i)
                        to_email = i.replace("TO-", "")
                        print("Recipient: " + to_email)
                        email_body = sms_message
                        print("Message: " + email_body)
                        print("Sending email via SMTP")
                        email_send(to_email, email_body)
                        
                    else:
                        print("TO- in message, no @, not sending email")
    if 'A-' in sms_message:
        for ai in sms_message.split():
                    if ai.startswith("A-"):
                        #print(i)
                        aprs_dest = ai.replace("A-", "")
                        print("APRS Destination: " + aprs_dest)
                        aprs_msg_body = sms_message.replace("A-" + aprs_dest, "")
                        print("APRS Message: " + aprs_msg_body)
                        print("Sending APRS message via APRS-IS")
                        aprs_send_msg(aprs_dest, aprs_msg_body.strip('\n'))
    else:
            print("Nothing received or recognized.")
            print("Exiting main()")


#############################################----APRS Functions----#############

global AIS, aprs_message_packet

aprs_message_packet = None

AIS = aprslib.IS(hotspot_callsign, passwd=aprs_passcode, port=14580)

def aprs_ack():
    global AIS
    print('Send ACK')
    time.sleep(1)
    print('Connecting to APRS-IS')
    AIS.connect()
    time.sleep(1)
    print('Sending...')
    AIS.sendall(hotspot_callsign + '>APRS,TCPIP*:' + ':' + parse_packet['from'] +' :ack'+parse_packet['msgNo'])
    print(hotspot_callsign + '>APRS,TCPIP*:' + ':' + parse_packet['from'] +': ack'+parse_packet['msgNo'])
    time.sleep(1)
    #AIS.close()
    #time.sleep(1)

def aprs_send_msg(aprs_to, aprs_message_text):
    global aprs_message_packet
    #print(aprs_to)
    #print(aprs_message_text.strip('\n'))
    #b_msg_num = len(aprs_message_text)
    aprs_message_number = str(len(aprs_message_text))
    if len(aprs_to) < 9: 
        aprs_to_spaces = aprs_to.ljust(9)
    if len(aprs_to) == 9:
        aprs_to_spaces = aprs_to
    else:
        print('greater than 9')
        aprs_to_spaces = aprs_to.ljust(9)
    aprs_message_packet = hotspot_callsign + '>APRS,TCPIP*:' + ':' + aprs_to_spaces +':'+ aprs_message_text + '{' + aprs_message_number
    #print(aprs_to_spaces)
    print('Connecting to APRS-IS')
    AIS.connect()
    time.sleep(1)
    print('Sending...')
    AIS.sendall(aprs_message_packet)
    print(aprs_message_packet)
    #time.sleep(1)
    #AIS.close()
                      
    

    
def aprs_location():
    location_packet = hotspot_callsign + '>APRS,TCPIP*:' + '=' + latitude + '/' + longitude + aprs_symbol + aprs_symbol_table + 'A=' + altitude + ' ' + aprs_comment
    print('Sending location packet.')
    print(location_packet)
    AIS.sendall(location_packet)
    
def aprs_beacon_1():
    beacon_1_packet = hotspot_callsign + '>APRS,TCPIP*:' + '=' + latitude + '/' + longitude + aprs_symbol + aprs_symbol_table + 'A=' + altitude + ' ' + aprs_beacon_1_comment
    print('Sending beacon 1 packet.')
    print(beacon_1_packet)
    AIS.sendall(beacon_1_packet)

def aprs_beacon_2():
    beacon_2_packet = hotspot_callsign + '>APRS,TCPIP*:' + '=' + latitude + '/' + longitude + aprs_symbol + aprs_symbol_table + 'A=' + altitude + ' ' + aprs_beacon_2_comment
    print('Sending beacon 1 packet.')
    print(beacon_2_packet)
    AIS.sendall(beacon_2_packet)

def aprs_receive_loop(packet):
        global parse_packet, aprs_message_packet, AIS
        # convert bytes to utf-8 string, ignore errors from non utf-8 bytes
        pak_str = packet.decode('utf-8',errors='ignore').strip()
        # Parse packet into dictionary
        parse_packet = aprslib.parse(pak_str)
        # Message ACK packet
        #aprs_msg_ack = hotspot_callsign + '>APRS,TCPIP*:' + ':' + parse_packet['from'] +':ack' + parse_packet['msgNo']
        # Retrieve value from dictionary key
        #print(par_pak['from'])

        if 'addresse' in parse_packet:
                if 'message_text' in parse_packet:
                        if hotspot_callsign == parse_packet['addresse']:
                            #AIS.close()
                            print('APRS message: ' + parse_packet['message_text'] + 'from: ' + parse_packet['from'])
                            aprs_ack()
                            # "dirty" fix to use single connection to APRS-IS, just put code of ack function here
                            #print('Send ACK')
                            #time.sleep(1)
                            #print('Connecting to APRS-IS')
                            #AIS.connect()
                            #time.sleep(1)
                            #print('Sending...')
                            #AIS.connect()
                            #AIS.sendall(hotspot_callsign + '>APRS,TCPIP*:' + ':' + parse_packet['from'] +' :ack'+parse_packet['msgNo'])
                            #print(hotspot_callsign + '>APRS,TCPIP*:' + ':' + parse_packet['from'] +': ack'+parse_packet['msgNo'])
                            #time.sleep(1)
                          ############################################
                            # Send message to DMR SMS
                            print(time.strftime('%H:%M:%S - %m/%d/%Y'))
                            shark.do_send_sms('1', '2', '9', '1','APRS MSG from: ' + parse_packet['from'] + '. ' + parse_packet['message_text'])
                            print('5 second reset')
                            time.sleep(5)
                            #AIS.connect()
                            #dmr_sms_aprs_reply = 'APRS MSG from: ' + parse_packet['from'] + '. ' + parse_packet['message_text']
                            #reply_sms(dmr_sms_aprs_reply)
                            time.sleep(1)
                            
                        else:
                                print('Na')
                else:
                    print('Message from: ' + parse_packet['from'] + ' To: ' + parse_packet['addresse'])
        #if aprs_message_packet != None:
        #    time.sleep(1)
         #   print('Sending...')
         #   AIS.sendall(aprs_message_packet)
         #   aprs_message_packet = None
        else:
            print('Packet from: ' + parse_packet['from'])
            #print(aprs_message_packet)


    #################################################
