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

# E-Mail checking loop. 
# https://github.com/kf7eel/shark-py-sms

# Feel free to modify and improve.

from core import *
#from shark import *
shark.do_login()

def main_loop():
    print('\n')
    print(time.strftime('%H:%M:%S - %m/%d/%Y'))
    shark.do_checkauth()
    print('Checking E-Mail')
    try:
        get_email()
    except:
        print('No configured account or an error occurred.')
        pass
    time.sleep(5)
    
while 1 < 5:
    try:
        main_loop()
    except:
        time.sleep(5)
        print('Exception, Pausing for 5 seconds...')
        shark.do_login()
        main_loop()
    finally:
        time.sleep(5)
        print('Final Exception, Pausing for 5 seconds...')
        shark.do_login()
        main_loop()


