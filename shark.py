#!/usr/bin/python3.7

######
# Original script authored by Scott Arnold, KD0KKV. The original can be found at https://github.com/battlehax/shark-py.
#
# Thanks Scott for letting me use your code!
#
# This script is heavily modified from the original found above.
#
######


# Updated code to reflect usage of JSON Web Tokens by the OpenSpot frimware as of 6-2018.
# Changed all items related to gathering information to GET requests as opposed to POST.
# Updated some code to reflect Python 3.7 compatability


#########
# THIS VERSION OF shark.py IS FOR USE WITH AUTO SETUP SCRIPT FOR SHARK-PY-SMS, IT HAS SOME VARIABLES MISSING ON PURPOSE.
# WILL NOT WORK BY ITS SELF.
#########

from config import *

import requests, json, re, binascii, hashlib

# password = 'openspot'
# ip = '10.10.10.132'
tmp = '/tmp/.shark.auth'
auth_file = '/tmp/.shark.jtw'
sms_msg = '/tmp/.shark.sms'
sms_msg_only = '/tmp/.shark.sms_only'
#hotspot_id = '9998' # HAS TO MATCH "SOURCE ID" in DMR SMS PAGE!

utf_8_url = str("http://"+ip+"/gettok.cgi").encode('utf-8')

def do_checkauth():
   global post
   try:
      f_auth = open(auth_file, 'r',encoding='utf-8')
      auth_text = f_auth.read()
      header = { 'Authorization': 'Bearer ' + auth_text }
      login = requests.post("http://"+ip+"/checkauth.cgi", headers=header)
      print((json.loads(login.text)['success']))
      if int(json.loads(login.text)['success']) != 1:
         return(do_login())
      else:
         return
   except:
         return(do_login())

def do_login():
   global tok, digest, post
   r = requests.post(utf_8_url)
   tok = r.json()['token']
   #tok = non_tok.encode('utf-8')
   #utf8_password = str(password).encode('utf8')
   digest = hashlib.sha256(tok.encode('utf-8') + password.encode('utf-8')).hexdigest()
   post = { 'token': tok, 'digest': digest }
   login = requests.post("http://"+ip+"/login.cgi", json=post)
   f = open(auth_file, 'w')
   f.write(json.loads(login.text)['jwt'])
   f.close
   return


def get_freq():
   rfreq = requests.post("http://"+ip+"/modemfreq.cgi", json=post)
   rx = rfreq.json()["rx_frequency"]
   tx = rfreq.json()["tx_frequency"]
   rx = str(rx / 1000000.0) + "MHz"
   tx = str(tx / 1000000.0) + "MHz"
   return{ 'rx': rx, 'tx': tx }

def get_status():
   f_auth = open(auth_file, 'r')
   auth_text = f_auth.read()
   header = { 'Authorization': 'Bearer ' + auth_text }
   rstatus = requests.get("http://"+ip+"/status.cgi", headers=header)
   room = rstatus.json()["connected_to"]
   status = rstatus.json()["status"]
   print(status)
   if status == 0:
      status = "Standby"
   elif status == 1:
      status = "In call"
   elif status == 3:
      status = "Connector not set"
   elif status == 4:
      status = "Modem initializing"
   elif status == 5:
      status = "Modem disconnected"
   elif status == 6:
      status = "Modem HW/SW version mismatch"
   elif status == 7:
      status = "Modem firmware upgrade in progress"
   else:
      status = "API ERROR: unknown status code"
   return{ 'status': status, 'room': room }

def get_mode():
   f_auth = open(auth_file, 'r')
   auth_text = f_auth.read()
   header = { 'Authorization': 'Bearer ' + auth_text }
   rmode = requests.get("http://"+ip+"/modemmode.cgi", headers=header)
   mode = rmode.json()["mode"]
   print(mode)
   if mode == 0:
      mode = "Idle"
   elif mode == 1:
      mode = "Raw"
   elif mode == 2:
      mode = "DMR"
   elif mode == 3:
      mode = "D-STAR"
   elif mode == 4:
      mode = "C4FM"
   else:
      mode = "API ERROR: unknown modem mode"
   submode = rmode.json()["submode"]
   if submode == 0:
      submode = "No submode"
   elif submode == 1:
      submode = "DMR Hotspot"
   elif submode == 2:
      submode = "DMR MS"
   elif submode == 3:
      submode = "DMR BS"
   else:
      submode = "API ERROR: unknown sub mode"
   return{ 'mode': mode, 'submode': submode }
   print(mode)

def get_connector():
   f_auth = open(auth_file, 'r')
   auth_text = f_auth.read()
   header = { 'Authorization': 'Bearer ' + auth_text }
   rconnector = requests.get("http://"+ip+"/connector.cgi", headers=header)
   connector = rconnector.json()["active_connector"]
   if connector == 0:
      connector = "No connector"
   elif connector == 1:
      connector = "DMRplus"
   elif connector == 2:
      connector = "Homebrew"
   elif connector == 3:
      connector = "TS repeat"
   elif connector == 4:
      connector = "DCS/XLX"
   elif connector == 5:
      connector = "FCS"
   elif connector == 6:
      connector = "SharkRF Client"
   elif connector == 7:
      connector = "SharkRF Server"
   elif connector == 8:
      connector = "DMR calibration"
   elif connector == 9:
      connector = "REF/XRF"
   elif connector == 10:
      connector = "YSF Reflector"
   else:
      connector = "API ERROR: unknown connector type" 
   return(connector)

def get_homebrew():
   f = open(auth_file, 'r')
   auth_text = f.read()
   header = { 'Authorization': 'Bearer ' + auth_text }
   r = requests.get("http://"+ip+"/homebrewsettings.cgi", json=post, headers=header)
   print(r)
   print((r.json()))
   return( r.json() )

def set_talkgroup(new_group):
   f_auth = open(auth_file, 'r')
   auth_text = f_auth.read()
   header = { 'Authorization': 'Bearer ' + auth_text }
   post = { 'new_autocon_id': new_group, 'new_c4fm_dstid': new_group, 'new_reroute_id': new_group }
   de = requests.post("http://"+ip+"/homebrewsettings.cgi", json=post, headers=header)
   return(json.loads(de.text)['changed'])

def set_freq( new_rx_freq, new_tx_freq = 1 ):
   new_rx_freq = float(new_rx_freq) * 1000000
   if new_tx_freq == 1:
      new_tx_freq = new_rx_freq
   else:
      new_tx_freq = float(new_tx_freq) * 1000000
   post = { 'token': tok, 'digest': digest, 'new_rx_freq': new_rx_freq, 'new_tx_freq': new_tx_freq }
   dc = requests.post("http://"+ip+"/homebrewsettings.cgi", json=post)
   return( int(json.loads(dc.text)['changed']) ) 

def set_mode( new_mode ):
   if new_mode == "dmr":
      newmode = 2
   elif new_mode == "dstar":
      newmode = 3
   elif new_mode == "c4fm":
      newmode = 4
   elif new_mode == "raw":
      newmode = 1
   elif new_mode == "idle":
      newmode = 0
   else:
      return("MODE ERROR: try one of dmr, dstar, c4fm, raw, idle")
   if newmode == 2:
      post = { 'token': tok, 'digest': digest, 'new_mode': newmode, 'new_submode': '1' }
   else:
      post = { 'token': tok, 'digest': digest, 'new_mode': newmode, 'new_submode': '0' }
   dm = requests.post("http://"+ip+"/modemmode.cgi", json=post)
   if int(json.loads(dm.text)['changed']) != 1:
      return("MODE ERROR: cannot change mode")

def do_send_sms( sms_type, sms_format, dstid, modem, msg ):
    only_save = "0"
    intercept_net_msgs = incoming_network_messages # Will add option later, 1 means incoming network messages are processed, 0 = not processed
# Replaced default values with input variable. Use quotes to restore default values
    send_calltype = sms_type # 0=Private, 1=TalkGroup
    send_srcid = hotspot_id
    send_format = sms_format #MD-380/390 is 1
    send_tdma_channel = "1"
    send_to_modem = modem #0=Network, 1=Modem
    msg_bytes = str.encode(msg)
    encoded = "".join([str('00' + x) for x in re.findall('..',bytes.hex(msg_bytes))] )
    #print(encoded)
    f = open(auth_file, 'r')
    auth_text = f.read()
# Changed character count from 150 to 300, this is to accomodate pairs as opposed to individual characters.
    if len(encoded) > 448:
      return("Message too long")
    post = { 'only_save': only_save, 'intercept_net_msgs': intercept_net_msgs, 
'send_dstid': dstid, 'send_calltype': send_calltype, 'send_srcid': send_srcid, 'send_format': send_format, 'send_tdma_channel': send_tdma_channel, 'send_to_modem': send_to_modem, 'send_msg': encoded.upper() }
    header = {'Authorization': 'Bearer ' + auth_text }
    requests.post("http://"+ip+"/status-dmrsms.cgi", json=post, headers=header)
    rq = requests.post("http://"+ip+"/status-dmrsms.cgi", json=post, headers=header)
#    print(rq)
#    print(post)
    print(("Destination: " + dstid))
    print(encoded)
#    print(auth_text)

def do_recieve_sms():
   f = open(auth_file, 'r')
   auth_text = f.read()
   header = { 'Authorization': 'Bearer ' + auth_text }
   r = requests.get("http://"+ip+"/status-dmrsms.cgi", headers=header)
#   print(r)
   sms_sender = str(json.loads(r.text)['rx_msg_srcid']) # Sender DMR ID of SMS
   sms_message_hex = ''.join(json.loads(r.text)['rx_msg'].split('00')) # The actual text of SMS, decoded
   sms_message = bytes.fromhex(sms_message_hex).decode('utf-8')
   sms_format = str(json.loads(r.text)['rx_msg_format']) # 0 - ETSI, 1 - UDP, 2 - UDP/Chinese
   sms_type = str(json.loads(r.text)['rx_msg_calltype']) # 0 = private, 1 = group
   sms_modem = str(json.loads(r.text)['rx_msg_from_modem']) # 0 = modem, 1 = Network
   f_msg = open(sms_msg, 'w')
   f_msg.write(sms_type)
   f_msg.write('\n')
   f_msg.write(sms_format)
   f_msg.write('\n')
   f_msg.write(sms_sender)
   f_msg.write('\n')
   f_msg.write(sms_message)
   f_msg.write('\n')
   f_msg.write(sms_modem)
   f_msg.write('\n')
   f_msg.close()
   f_msg_only = open(sms_msg_only, 'w')
   f_msg_only.write(sms_message)
   f_msg_only.close()

#   print(sms_sender)
#   print(sms_message)
   if sms_message != '':
      return([ sms_sender, sms_message ])

def get_ip():
   r = requests.post("http://"+ip+"/ip.cgi", json=post)
   shark_ip = str(json.loads(r.text)['ip'])
   return(shark_ip)
