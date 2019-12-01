# shark-py-sms

----

Place these files in the same folder as the shark-py files. shark-py must be the version here (https://github.com/kf7eel/shark-py) to work these scripts.
This will work with Openspot firmware 0101 or later as all versions after 0101 use JSON Web Tokens.


----
### sms-interact.py

This is the main script and contains all the core functionality. (It runs in a loop, so there is no need for a scheduled cron job.)

----
### Current Status - 11/29/2019

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


#### Features

* SMS to E-Mail
* E-Mail to SMS
* Current Time
* Echo SMS back to user

Currently working on implementing:

* APRS messaging functionality
* Commands to control Openspot

Future possible features:

* Some sort of XMPP implimentation.

#### TODO

* Finish cleaning up email functions.
* Start coding APRS messaging functionality using APRS lib.

----
### Requirements

First and formost, my modified shark-py "library" is required. I took the shark-py code, originally published by battlehax (https://github.com/battlehax/shark-py), and updated the authentication mechanism to support JSON Web Tokens, as Openspot firmware 0101 and later requires this to use the Shark API. I have also updated some of the code to make it compatable with Python 3.7. #### *Find it at https://github.com/kf7eel/shark-py .

This script also requires the follwing Python modules:
re, binascii, shark, time, os, datetime, smtplib, email, poplib

which should be included on any modern Linux distrobution.

----
### Installation

Download this repository into the same folder as shark-py, found at https://github.com/kf7eel/shark-py.

Install all necessary python modules.

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
This script will check for moderate, severe, or extreme weather alerts and send them to the configured sms receiver.
Setting this up to send to a talk group will allow multiple users to receive severe weather alerts.

Requires the python module WeatherAlerts. https://weatheralerts.readthedocs.io/en/latest/about.html
