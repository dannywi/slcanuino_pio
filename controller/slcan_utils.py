'''
Helper functions to do communications to Serial Line CAN device
'''

import serial
from enum import Enum
import slcan_converter as sc

def _send(ser, msg):
  ser.write(msg.encode('utf-8'))

def cmd_open_channel(ser):
  _send(ser, '0')

def cmd_close_channel(ser):
  _send(ser, 'C')

def cmd_toggle_timestamp(ser, flag):
  c = '0' if flag is False else '1'
  _send(ser, 'Z' + c)

def cmd_send_accept_mask(ser):
  _send(ser, 'M')

def cmd_send_accept_value(ser):
  _send(ser, 'm')

_bit_rate = {
  'CANSPEED_100': '3',
  'CANSPEED_125': '4',
  'CANSPEED_250': '5',
  'CANSPEED_500': '6',
  'CANSPEED_800': '7',
  'CANSPEED_1000': '8',
}

def send_bit_rate(ser, val):
  if val in _bit_rate:
    _send(ser, 'S' + _bit_rate[val])

def send_status_req(ser):
  _send(ser, 'F')

def send_version_req(ser):
  _send(ser, 'V')

def send_serial_num_req(ser):
  _send(ser, 'N')

def send_can_frame(ser, id, data, is_ext = False, is_rtr = False):
  msg = sc.convert_to_slcan(id, data, is_ext, is_rtr)
  if len(msg) > 0:
    _send(ser, msg)
  else:
    print("FAILED to send can msg: id {}".format(hex(id)))