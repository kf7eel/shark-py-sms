#!/usr/bin/python3.7

###############################################################################
#   Copyright (C) 2020 Eric Craw, KF7EEL <kf7eel@qsl.net>
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

# Modified 04-19-2020, by Eric, KF7EEL

# Contains all functions for program
# APRS-IS receive script and required by Interactive SMS script. 
# https://github.com/kf7eel/shark-py-sms

# Feel free to modify and improve.

# Import modules
# DMR SMS
from config import *
from user_commands import *
from system_commands import *
#from user_functions import *
import user_functions
import system_commands
import re, binascii, shark, time, os, datetime, smtplib, random
import email, poplib
from email.header import decode_header
# APRS
import aprslib, logging
import csv

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
        sms_modem = data[4]
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
            print("Sent from: (0 = network, 1 = modem): " + sms_modem)
            if sms_modem == '0':
                print('Network')
            if sms_modem == '1':
                print('RF Modem')
            print('\n' + "--------------------------------------" + '\n')

def reply_sms(message):
    global sms_type, sms_format, sms_source, sms_modem, sms_message, network_reply_mode
    print('\n')
    print("Sending SMS reply...")
    print('\n')
    time.sleep(2)
    if talkgroup_reply_mode == 0:
        shark.do_send_sms(sms_type, sms_format, sms_source, sms_modem, message)
    # For testing purposes, below is set to group SMS due to issues with AT-D878. o_ indicates override, see above
    else:
        shark.do_send_sms(o_sms_type, o_sms_format, o_sms_source, sms_modem, message)
    print("SMS type: " + sms_type)
    print("Format: " + sms_format)
    print("Source: " + sms_source)
    print("Message: " + message)
    print('Modem/Network (0 = network, 1 = modem): ' + sms_modem)
    if sms_modem == 0:
        print('Network')
    if sms_modem == 1:
        print('RF Modem')
    #print('Network Reply - 0 = off, 1 = on: ' + str(network_reply_mode))
    if str(network_reply_mode) == '0':
        print('Network reply disabled.')
    if str(network_reply_mode) == '1':
        print('Network reply enabled.')
        


def tg_sms_send(message):	
	    global tg_sms	
	    print('Sending SMS to talkgroup ' + tg_sms)	
	    time.sleep(1)	
	    if network_reply_mode == 1:	
	        sms_modem = 0	
	    if network_reply_mode == 0:	
	        sms_modem = 1	
	    print('Mode selected')	
	    if tg_sms_all_formats == 1:	
	        print('Sending in ETSI format')	
	        shark.do_send_sms(o_sms_type, '0', tg_sms, sms_modem, message)	
	        time.sleep(10)	
	        print('Sending in UDP format')	
	        shark.do_send_sms(o_sms_type, '1', tg_sms, sms_modem, message)	
	        time.sleep(10)	
	        print('Sending in UDP/Chinese format')	
	        shark.do_send_sms(o_sms_type, '2', tg_sms, sms_modem, message)	
	    if tg_sms_all_formats == 0:	
	        shark.do_send_sms(o_sms_type, o_sms_format, tg_sms, sms_modem, message)	
	    time.sleep(1)	
	
    

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
                        # Email to specific DMR ID not implimented yet, send to talkgroup 9
                        shark.do_send_sms(o_sms_type, o_sms_format, o_sms_source, sms_modem, dmr_email_msg)
                        print('Deleting message')
                        pop_server.dele(del_msg)
                        #break
    pop_server.quit()

def main():
    global data, sms_type, sms_format, sms_source, sms_message, sms_modem
    # Commands are here
    # line_break vairable used due to how string processed in python, defined above

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

                
# Look for command in dictionary, user defined
    else:
        for key in cmd_list:
            if key + line_break == sms_message:
                print('User defined command: ')
                print(cmd_list[key])
                cmd_list[key]()
                return

    if 'A-' in sms_message:
        for ai in sms_message.split():
                    if ai.startswith("A-"):
                        #print(i)
                        aprs_dest = ai.replace("A-", "")
                        print("APRS Destination: " + aprs_dest)
                        aprs_msg_body = sms_message.replace("A-" + aprs_dest, "")
                        print("APRS Message: " + aprs_msg_body)
                        print("Sending APRS message via APRS-IS")
                        #aprs_send_msg(aprs_dest, aprs_msg_body.strip('\n'))
                        dmr_to_aprs_send(aprs_dest, aprs_msg_body.strip('\n'))
    else:
            print("Nothing received or recognized.")
            print("Loop reset")

    if '!' + line_break == sms_message:
        reply_sms('Unknown')
    if 'ADD-' in sms_message:
        aprs_call = re.sub("ADD-", "", sms_message)
        aprs_map_add(aprs_call)
        reply_sms('APRS Callsign ' + aprs_call + ' mapped to DMR ID ' + sms_source)
        
    if 'DEL-' in sms_message:
        delete_call = re.sub("DEL-", "", sms_message)
        print(delete_call)
        aprs_map_del(delete_call)
        reply_sms('Deleted APRS call: ' + delete_call + ' from database.')
# Look for command in dictionary, system commands
    else:
        for sys_key in sys_cmd_list:
            if sys_key + line_break == sms_message:
                print('System command: ')
                print(sys_cmd_list[sys_key])
                sys_cmd_list[sys_key]()
                return
            #else:
            #    print('Command not defined')

#############################################----APRS Functions----#############

global AIS, aprs_message_packet

aprs_message_packet = None

#AIS = aprslib.IS(hotspot_callsign, passwd=aprs_passcode, port=14580)

#AIS_send = aprslib.IS(hotspot_callsign, passwd=aprs_passcode, host='rotate.aprs2.net', port=14580)

		
AIS_send = aprslib.IS(hotspot_callsign, passwd=aprs_passcode,host='rotate.aprs2.net', port=14580)	
        
AIS = aprslib.IS(hotspot_callsign, passwd=aprs_passcode, host=aprs_is_host, port=aprs_is_port)	
        
# YAAC TCP send function	
def yaac_aprs_tcp_send(yaac_msg_source, yaac_msg_dest, yaac_message):	
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)	
    host = yaac_host #socket.gethostname()                           	
    port = yaac_port	
# connection to hostname on the port.	
    s.connect((host, port))                               	
#msg = 'KF7EEL>KF7EEL-7:testing again...{27'+'\r'	
    yaac_msg = yaac_msg_source + '>APRS::' + yaac_msg_dest.ljust(9) + ':' + yaac_message + '{' + str(len(aprs_message_text)) + time.strftime('%s') + '\r'	
# Working packet!	
# msg = 'KF7EEL-15>APRS::KF7EEL-7 :test 23{23'+'\r'                              	
    s.send(msg.encode('ascii'))	
    s.close()

def aprs_ack():	
    global AIS	
    print('Send ACK')	
    time.sleep(1)	
    if use_yaac == 0:
        if 'msgNo' in parse_packet:
            print('Send ACK')
            time.sleep(1)
            print('Connecting to APRS-IS')
            AIS_send.connect()
            time.sleep(1)
            print('Sending...')
            AIS_send.sendall(hotspot_callsign + '>APRS,TCPIP*:' + ':' + parse_packet['from'].ljust(9) +' :ack'+parse_packet['msgNo'])
            print(hotspot_callsign + '>APRS,TCPIP*:' + ':' + parse_packet['from'] +': ack'+parse_packet['msgNo'])
            time.sleep(1)
        else:
            print('No ACK reqd.')
##        print('Connecting to APRS-IS')	
##        AIS_send.connect()	
##        time.sleep(1)	
##        print('Sending...')	
##        from_space = parse_packet['from']	
##        AIS_send.sendall(hotspot_callsign + '>APRS,TCPIP*:' + ':' + from_space.ljust(9) + ':ack'+parse_packet['msgNo'])	
##        print(hotspot_callsign + '>APRS,TCPIP*:' + ':' + from_space.ljust(9) + ':ack'+parse_packet['msgNo'])	
##        time.sleep(1)	
##        AIS_send.close()	
        #time.sleep(1)	
    if use_yaac == 1:	
        print('todo')


def aprs_send_msg(aprs_to, aprs_message_text):
    global aprs_message_packet
    #print(aprs_to)
    #print(aprs_message_text.strip('\n'))
    #b_msg_num = len(aprs_message_text)
    # Generate message number by adding character count to number and dding current time in seconds. Dirty, but works.
    aprs_message_number = str(len(aprs_message_text)) + time.strftime('%s')
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
    AIS_send.connect()
    time.sleep(1)
    print('Sending...')
    AIS_send.sendall(aprs_message_packet)
    print(aprs_message_packet)
    #time.sleep(1)
    AIS.close()

def aprs_map_add(aprs_callsign):
    with open(map_csv, "a") as myfile:
            myfile.write('' + str(aprs_callsign).strip('\n') + ',' + str(sms_source).strip('\n') + ',' + str(sms_format).strip('\n') + ',' + str(sms_modem).strip('\n') + '\n')
            
def aprs_map_del(del_call):
    with open(map_csv, "r") as f:
        lines = f.readlines()
        print(lines)
##        print('-------')
    with open(map_csv, "w") as f:
        for line in lines:
            #print(re.sub(",.*", "", line))
            #if line.strip("\n") != aprs_call: # not in line:
            if str(re.sub(",.*", "", line)).strip("\n") != str(del_call).strip("\n"):
                f.write(line)
    
def dmr_to_aprs_send(aprs_to, aprs_message_text):
    global sms_source
    aprs_message_number = str(random.randint(1,99)) + str(random.randint(1,9))
    with open(map_csv, 'rt') as map_file:
        map_send = csv.reader(map_file)
        for map_line in map_send:
            #print(map_line[1] + ' ' + sms_source)
            #print(type(map_line[1]))
            #print(type(sms_source))
            if map_line[1] in sms_source:
                    print('Found DMR ID in map.')
                    if len(aprs_to) < 9:
                        aprs_to_spaces = aprs_to.ljust(9)
                    if len(aprs_to) == 9:
                        aprs_to_spaces = aprs_to
                    else:
                        print('greater than 9, trimming to fit...')
                        aprs_to_spaces = aprs_to.ljust(9)
                    dmr_to_aprs_message_packet = map_line[0] + '>APRS,TCPIP*:' + ':' + aprs_to_spaces +':'+ aprs_message_text #+ '{' + aprs_message_number <----- this will force other station to ack
                    print('Connecting to APRS-IS')
                    AIS_send.connect()
                    time.sleep(1)
                    print('Sending...')
                    print(dmr_to_aprs_message_packet)
                    AIS_send.sendall(dmr_to_aprs_message_packet)
                    break
        else:
            if len(aprs_to) < 9: 
                aprs_to_spaces = aprs_to.ljust(9)
            if len(aprs_to) == 9:
                aprs_to_spaces = aprs_to
            else:
                print('greater than 9')
                aprs_to_spaces = aprs_to.ljust(9)
                             #print(aprs_to_spaces)
            print('DMR ID not found')
            print('|' + map_line[0] + '|' + ' - ' + '|' + map_line[1] + '|')

            print('Connecting to APRS-IS')
            AIS_send.connect()
            aprs_message_packet = hotspot_callsign + '>APRS,TCPIP*:' + ':' + aprs_to_spaces +':'+ aprs_message_text + '{' + aprs_message_number
            time.sleep(1)
            print('Sending...')
            AIS_send.sendall(aprs_message_packet)
            print(aprs_message_packet)


    
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
    global parse_packet, aprs_message_packet, AIS_send

        # Message ACK packet
        #aprs_msg_ack = hotspot_callsign + '>APRS,TCPIP*:' + ':' + parse_packet['from'] +':ack' + parse_packet['msgNo']
        # Retrieve value from dictionary key
        #print(par_pak['from'])
#######
        # convert bytes to utf-8 string, ignore errors from non utf-8 bytes
    pak_str = packet.decode('utf-8',errors='ignore').strip()
        # Parse packet into dictionary
    parse_packet = aprslib.parse(pak_str)
    with open(map_csv, 'rt') as map_file:
            map_read = csv.reader(map_file)
######
            if 'bulletin' in parse_packet['format']:	
	                print('Bulletin Received...')	
	                print('Bulletin from: ' + parse_packet['from'] + ' Message: ' + parse_packet['message_text'])	
	                tg_sms_send('Bulletin from: ' + parse_packet['from'] + ' Message: ' + parse_packet['message_text'])	
	                time.sleep(3)
            if 'addresse' in parse_packet:
                   if 'message_text' in parse_packet:
                            for map_line in map_read:
                                if map_line[0] == parse_packet['addresse']:
                                    print('yep')
                                    print(map_line[0])
                                    print('APRS message: ' + parse_packet['message_text'] + ' From: ' + parse_packet['from'] + 'To: ' + map_line[0])
                                    # Begin ACK with APRS call of recipient
                                    if 'msgNo' in parse_packet:
                                        print('Send ACK')
                                        time.sleep(1)
                                        print('Connecting to APRS-IS')
                                        AIS_send.connect()
                                        time.sleep(1)
                                        print('Sending...')
                                        AIS_send.sendall(map_line[0] + '>APRS,TCPIP*:' + ':' + parse_packet['from'] +' :ack'+parse_packet['msgNo'])
                                        print(map_line[0] + '>APRS,TCPIP*:' + ':' + parse_packet['from'] +': ack'+parse_packet['msgNo'])
                                    else:
                                        print('no ack')
                                    ### End Ack
                                    time.sleep(2)
                                    print(time.strftime('%H:%M:%S - %m/%d/%Y'))
                                    #set to send to network or modem in config
                                    shark.do_send_sms('0', map_line[2], map_line[1], aprs_tg_network_reply,'APRS MSG from: ' + parse_packet['from'] + '. ' + parse_packet['message_text'])
                                    print(map_line[0] + ' type: ' + map_line[2] + ' dst: ' + map_line[1])
                                    print('5 second reset')
                                    time.sleep(5)

                            if hotspot_callsign == parse_packet['addresse']:
                                print('APRS message: ' + parse_packet['message_text'] + ' From: ' + parse_packet['from'])
                                aprs_ack()
                            # Send message to DMR SMS
                                print(time.strftime('%H:%M:%S - %m/%d/%Y'))
                                # send to network or modem defined in config
                                shark.do_send_sms('1', '2', '9', aprs_tg_network_reply,'APRS MSG from: ' + parse_packet['from'] + '. ' + parse_packet['message_text'])
                                print('5 second reset')
                                time.sleep(5)
                            #AIS.connect()
                            #dmr_sms_aprs_reply = 'APRS MSG from: ' + parse_packet['from'] + '. ' + parse_packet['message_text']
                            #reply_sms(dmr_sms_aprs_reply)
                                time.sleep(1)
                            
                            else:
                                    print('...')
                    #else:
                     #   print('Message from: ' + parse_packet['from'] + ' To: ' + parse_packet['addresse'])

            else:
                print('Packet from: ' + parse_packet['from'] + ' - ' + time.strftime('%H:%M:%S'))
            #print(aprs_message_packet)


    #################################################
