# Introduction

----

Place these files in the same folder as the shark-py files. shark-py must be the version here (https://github.com/kf7eel/shark-py) to work these scripts.
This will work with Openspot firmware 0101 or later as all versions after 0101 use JSON Web Tokens.


----
### sms-interact.py

This is the main script and contains all the core functionality. (It runs in a loop, so there is no need for a scheduled cron job.)

----
### Current Status - 12/6/2019

Just implimented DMR SMS to APRS gateway. Any DMR SMS that contains "A-" will be routed to APRS.
"A-" must contain APRS station, including. Example: "A-N0CALL-5 This is a test message." This will send an APRS message to N0CALL-5 (fiticious call) with a message of "This is a test message."


#### 12/5/2019

Just uploaded "Version 1.1". This contains alot of bug fixes, a restructuring of the code, and implemented APRS to DMR SMS functionality, complete with APRS ack of message. Current installation instructions may need some changinging. Hopefully someone will find this usefull. Next up, DMR SMS to APRS message.

#### 11/29/2019

Just upload initial script, still a little buggy.

Upon starting sms-interact.py, script will check Openspot for a new message, then it process any received SMS for a command.
Next, it will check for any new email, send any emails in Inbox to DMR radios, before waiting 5 seconds to repeat.


*Please note, it is reccomended to have a dedicated email account for this script. The script will look for any emails with subject "TO-", then process and send SMS to modem. Next, it will delete the email. In other words, any email with subject line beginning with "TO-" will be deleted.

To send an email via configured SMTP server, SMS must begin with "TO-" and have email address
attached with no space. The rest of the message is sent in the email body.
(example "TO-user@example.org This is a test." will result in an email to user@example.org containing
"TO-user@example.org This is a test." in the body.

Currently working to implement some type of APRS functionality and Openspot control commands.

#### Currently, script is configured by default to send SMS replies to Talkgroup 9.
This is due to an issue with the Anytone D878 used during testing. Sometimes the radio will not send an acknowledgement packet to the Openspot fast enough, resulting in 2-4 SMS messages. Further implimentation required for private SMS to be fully functional.

This script should also theoretically respond to SMS sent from the DMR network, however, I only have 1 hotspot and have not been able to test this. Will fully impliment response to network SMS in the future. At present, this capability is "half implimented."


# Features

* SMS to E-Mail
* E-Mail to SMS
* APRS to DMR SMS gateway (12/5/2019) 
* DMR SMS to APRS gateway (12/6/2019)
* Current Time
* Several minor commands

Currently working on implementing:

* DMR SMS to APRS 
12/5/2019 - Sucessfully implimented APRS to DMR SMS.
12/2/2019 - Sucessfully filtering packets from specific callsigns. Next, need to filter packet further for processing...

* Commands to control Openspot
12/5/2019 - Not yet started...

Future possible features:

* Some sort of XMPP implimentation.
* METAR info
* Have any ideas?

#### TODO

* Finish cleaning up email functions.
* Start coding APRS messaging functionality using APRS lib.

----

# Commands

Commands are in CAPS.

* HELP - displays help message, Returns in a series of 4 messages, use with caution
* ECHO - replies eniter message back to user
* TIME - current local time
* UPTIME - uptime of host system
* PING - replies with pong
* ID - returns your DMR ID
* If "TO-" and "@" are in message, will send email to address. Example:

`
TO-user@example.org This is a test message.
` 

will result in an email to user@example.org with a body of "This is a test message.
Replies to the email gateway MUST have entire message in Subject line, the body of the message is ignorred at this point. Example:

`
To: (email account configured in script)
Subject: Hello DMR SMS!
Body: bla bla
`

will result in a DMR SMS, "Hello DMR SMS!", sent to talkgroup 9. (Will impliment private SMS in near future.)

* If "A-" is in message, will send APRS message to specified station. Must include APRS SSID. Example:

`
A-kf7eel-2 This is a test message.
`

will result in an APRS message sent to "KF7EEL-2" with message of "This is a test message."
APRS replies will be sent to talkgroup 9, will impliment private DMR SMS shortly, just need to change a few lines of code...


----
# Requirements

First and formost, my modified shark-py "library" is required. I took the shark-py code, originally published by battlehax (https://github.com/battlehax/shark-py), and updated the authentication mechanism to support JSON Web Tokens, as Openspot firmware 0101 and later requires this to use the Shark API. I have also updated some of the code to make it compatable with Python 3.7. #### *Find it at https://github.com/kf7eel/shark-py .

This script also requires the follwing Python modules:
re, binascii, shark, time, os, datetime, smtplib, email, poplib

which should be included on any modern Linux distrobution.

### Openspot setup

The source id under the DMR SMS page must match the "hotspot_id" in shark.py.
SMS messages must be sent to that DMR ID, private SMS.

"tdma_channel" in shark.py must match the DMO channel in the connectors page, and the TDMA channel to which the openspot sends traffic to the network. TDMA channel = slot.

SMS page appears to only send on slot 1. 

When using send-sms.py in example, and every thing configured for Slot 2, it appears that Openspot sends group SMS to network in MMDVM mode... Hmm, interesting...

### Confirmed!
The Openspot will send SMS via HBLink3. Sent a network SMS and observer MMDVM_Bridge receive packet.

----
### Installation

Download this repository into the same folder as shark-py, found at https://github.com/kf7eel/shark-py.

1. Create folder for shark-py-sms

`
mkdir shark-py-sms
`

2. Download the modified shark-py, found at https://github.com/kf7eel/shark-py.

`
git clone https://github.com/kf7eel/shark-py.git shark-py-sms/
`

3. Download shark-py-sms.

`
git clone https://github.com/kf7eel/shark-py-sms.git py-sms
`

4. Move shark-py-sms files into same folder as shark-py.

`
cp -r py-sms/* shark-py-sms/
`

5. Open shark.py and edit neseccary lines: "ip", "passwrd", and "hotspot_id" to match your Openspot.

6. Open and modify sms-interact.py to match your email account and other settings.

7. Run:

`
python3.7 sms-interact.py
`

Install all necessary python modules if it complains about import errors.

That should be it.

----
### Configuration

Find the section of code in the "box" near the top of sms-interact.py and change to your settings.

Next, open shark.py and change the values, located near the top of the file, and fill in your Openspot ip address and password.

Now run:
python3.7 sms-interact.py.

You should be set.

----

### noaa.py - NWS Weather Alert to SMS

### Broken in Python 3.7... 
Appears to be an issue with the required module, will work on later...


This script will check for moderate, severe, or extreme weather alerts and send them to the configured sms receiver.
Setting this up to send to a talk group will allow multiple users to receive severe weather alerts.

Requires the python module WeatherAlerts. https://weatheralerts.readthedocs.io/en/latest/about.html
