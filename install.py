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

# Version "1.2", by Eric, KF7EEL

# Install script

import os
import subprocess

# Future implimentation
#print('Using apt to install dependencies...')
#os.system('sudo apt install wget git python3.7 python3-pip')
#print('Downloadinf latest shark-py-sms...')
#os.system('git clone https://github.com/kf7eel/shark-py-sms.git')
#os.system("pip3 install aprslib")
#print('Installing requirements...')



# Download shark.py
print('Downloading required library')
os.system('wget https://github.com/kf7eel/shark-py/raw/master/shark_sms_install_version.py')
print('Deleting old shark.py if it exists.')
os.system('rm shark.py')
print('Renaming to shark.py')
os.system('mv shark_sms_install_version.py shark.py')
print('Installing aprslib...')
os.system('pip3 install aprslib')
print('Moving sample config to config.')
os.system('cp config.SAMPLE config.py')
print('Installation complete. Please edit config.py to finish.')
