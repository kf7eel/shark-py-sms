#!/usr/bin/python

# Interactive SMS script, version "1.0", by Eric, KF7EEL
# https://github.com/kf7eel/shark-py-sms

# Feel free to modify and improve.

# Import modules

import re, binascii, shark, time, os, datetime, smtplib
import email, poplib
from email.header import decode_header


#--------------------------------------------------------#
# User, Password, and smtp server of your email account. #
email_user = 'email user  '                              #
email_password = 'Password  '                            #
email_server = 'Mail server'                             #
smtp_port = 465                                          #
pop_port = 995                                           #
#--------------------------------------------------------#

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

def sms_get():
    print("Checking for authorization...")
    shark.do_checkauth()
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
                        break
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
            current_time = time.strftime('%H:%M %A %B, %Y - Timezone: %z')
            reply_sms(current_time)
            
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
    else:
            print("Nothing received or recognized.")
            print("Restarting after 5 seconds...")


while 1 < 5:
    print(time.strftime('%H:%M:%S - %d/%m/%Y'))
    sms_get()
    sms_read()
    get_email()
    main()
    time.sleep(5)
