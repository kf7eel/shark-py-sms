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

# User defined functions. 
# https://github.com/kf7eel/shark-py-sms

# Feel free to modify and improve.

# 

def example():
    from core import reply_sms
    reply_sms('This is an example reply')
def example2():
    import core
    time.sleep(2)
    shark.do_send_sms( '1', '2','9', '0', 'this is an example' )
    time.sleep(2)
def example3():
    from core import reply_sms
    reply_sms('This is the final test')
