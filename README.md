# Introduction

----

This will work with Openspot firmware 0101 or later as all versions after 0101 use JSON Web Tokens.

----

# See Wiki for more info.
----
### 4/19/2020
Add ability to manage DMR ID to APRS callsign.
You can now send an SMS to add your radio DMR ID to the APRS callsign map.
"ADD-[your call with SSID]" will associate your DMR ID to your APRS callsign. All APRS messages sent to the call you entered will now be sent to your DMR radio, and all APRS messages sent from you DMR radio will have your APRS callsign.

"DEL-[your call wil SSID]" will remove your radio from the internal database.

#### 2/10/2020
I have updated the code. Made several stability improvements and added the ability to send bullitens received on APRS to a talk group.

I have also made the decision to focus the more innovative developement and features to an Interactive APRS script. APRS is more widely used, easier to implement due to the open standards, and is used on multiple platform, from D-Star to some DMR networks, and online. In terms of APRS, the focus going in this project will be more towards stability improvements with "bridging" APRS to DMR SMS. In other words, some functions will be moved to the Interactive APRS script, such as the E-Mail gateway and planned information services, such as weather. Not to fear though, there will still be plenty of work on additional features here.

#### 1/29/2020

I managed to track down the original author of the python script that communicates via API. He gave me permission to include the script with this project. This will make it significantly easier to setup. Thanks to Scott, KD0KKV, the original author of the python API script that made this project possible (Original found at https://github.com/battlehax/shark-py).

#### 1/13/20
Getting ready to upload some major changes. I have been focusing on making this program more easily usable for other users in the last several days. Separated most system commands out of the core and into a function file and command file, allowing users to customize them. Have added a user defined command file set as well, will have documentation coming on that part soon, to make it easy for users to add custom commands. Also presently rewriting the APRS portion to allow APRS messgaes to DMR SMS and vice versa, to multiple APRS SSIDs. The idea is to compliment the analog APRS features of the Anytond D878. You will be able to set the APRS SSID in the program, and have APRS messages passed to a specified DMR ID!

#### 1/8/10
Today I focused mostly on imporving the usability of the program. I added an exception handle to sms_loop for checking email, so if it fails, it won't stop the whole thing. This means now that an email account is no longer required. Also added to the configuration the option to enable or disable "network reply." This effectively makes the modem send SMS via RF only, and/or to network. A few changes in core.py and the shark.py library have allowed this.
 
 Added an option in config.py to enable or disable "talkgroup reply." This will send all SMS replie to talkgroup 9, modem side only. Used primarily for testing. See below for details.
 
I have modified the shark.py file in the other repository to work with an installation script to allow for a more seamless "experience" for the Openspot user. It is not fully complete, but work for installing the reqired file. Still working on a more complete installation script.

I have acquired a Pi-Star hotspot, and have been able to test the program network capabilities. It works just fine over network. HBLink3 is serving as the "test network."

Future implementations: User defined commands, persistent data storage for routing APRS, and APRS to email.

#### 12/6/2019

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

* 2 way DMR to E-Mail gateway 
* 2 way DMR to APRS messaging gateway
* Several commands
* User defined commands (work in progress)

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

* Finish cleaning up email functions and code funtion for E-Mail --> Private DMR SMS.


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

### Openspot setup notes and thing I discovered

The source id under the DMR SMS page must match the "hotspot_id" in shark.py.
SMS messages must be sent to that DMR ID, private SMS.

"tdma_channel" in shark.py must match the DMO channel in the connectors page, and the TDMA channel to which the openspot sends traffic to the network. TDMA channel = slot.

SMS page appears to only send on slot 1. 

When using send-sms.py in example, and every thing configured for Slot 2, it appears that Openspot sends group SMS to network in MMDVM mode... Hmm, interesting...

### Confirmed!
The Openspot will send SMS through HBLink3. Sent a network SMS and observer MMDVM_Bridge receive packet.

----

### noaa.py - NWS Weather Alert to SMS

### Broken in Python 3.7... 
Appears to be an issue with the required module, will work on later...


This script will check for moderate, severe, or extreme weather alerts and send them to the configured sms receiver.
Setting this up to send to a talk group will allow multiple users to receive severe weather alerts.

Requires the python module WeatherAlerts. https://weatheralerts.readthedocs.io/en/latest/about.html

----

### Automatic Packet Reporting System (APRS) was invented and is trademarked by Bob Bruninga, WB4APR.
