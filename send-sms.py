#!/usr/bin/python
import re, binascii, shark
#shark.do_login()
shark.do_checkauth()
shark.do_send_sms( '0', '1','9998', 'How long can this message be? 1234567' )

