#!/usr/bin/python
import re, binascii, shark
#shark.do_login()
shark.do_checkauth()
# First option is for calltype (0 - private, 1 - group), then format (0 - ETSI, 1 - UDP, 2 - UDP/Chinese).
# Third option is the destination DMR ID, send to modem (1) or network (0), and the last is the actual message.
shark.do_send_sms( '0', '1','9998', '1', 'How long can this message be? 1234567' )

