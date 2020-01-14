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

# Version "1.2.1", by Eric, KF7EEL

# System Functions. 
# https://github.com/kf7eel/shark-py-sms

# Feel free to modify and improve.

# Simple commands that do not require filtering


def initialize():
    import time, os
    from core import sms_type, sms_format, sms_source, sms_message, sms_modem
    global sms_type, sms_format, sms_source, sms_message, sms_modem

# Send user system uptime
def uptime():
    import time, os, core
    from core import reply_sms, sms_type, sms_format, sms_source, sms_message, sms_modem
    print('Getting uptime...')
    uptime = os.popen('uptime').read()
    reply_sms(str(uptime))

# Replies to user by sending what was received
def echo():
    import time, os, core
    from core import reply_sms, sms_type, sms_format, sms_source, sms_message, sms_modem
    reply_sms(sms_message)
    print("Echoing SMS")
# Return current time
def time():
    import time, os, core
    from core import reply_sms, sms_type, sms_format, sms_source, sms_message, sms_modem
    print('Getting time...')
    current_time = time.strftime('%H:%M %A %B %d, %Y - Timezone: %z')
    reply_sms(current_time)

def ping():
    from core import reply_sms, sms_type, sms_format, sms_source, sms_message, sms_modem
    import time, os, core
    print("Received ping...")
    time.sleep(0.5)
    print("Pong")
    reply_sms('Pong '+time.strftime('%H:%M:%S - %m/%d/%Y'))

def reply_dmr_id():
    from core import reply_sms, sms_type, sms_format, sms_source, sms_message, sms_modem
    import time, os, core
    print('DMR ID: '+ sms_source)
    reply_sms('Your DMR ID is ' + sms_source)

def command_help():
    from core import reply_sms, sms_type, sms_format, sms_source, sms_message, sms_modem
    import time, os, core
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

def send_dmr_to_aprs_mapped():
    import time, os, core
    from core import dmr_to_aprs_send
    try:
        dmr_to_aprs_send('TEST', 'This is a test')
    except:
        print('execute aprs_send here')
        

