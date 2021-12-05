import serial
import argparse
import re
import os
import time
from datetime import datetime
import slcan_utils as su
import slcan_converter as sc

can_msgs = [
  {
    "can_msg": {"id":0x674, "data":[0xff, 0xfe, 0x04, 0x31, 0x80, 0x12, 0xf9, 0xf8], "is_ext": False},
    "interval": 3,
    "prev_secs": 0,
    "count": 10,
  },
  {
    "can_msg": {"id":0x683, "data":[0xfa, 0xce, 0xfe, 0xed, 0xbe, 0xef, 0xca, 0xfe], "is_ext": False},
    "interval": 5,
    "prev_secs": 0,
    "count": 60,
  },
  {
    "can_msg": {"id":0x1ABC3333, "data":[0x12, 0x34, 0x56, 0x78, 0xab, 0xcd, 0xba], "is_ext": True},
    "interval": 5,
    "prev_secs": 0,
  },
]

def run(port, baud):
  ser = serial.Serial(
    port=port,
    baudrate=baud,
    timeout=0.2,
  )

  time.sleep(2); # give time to reboot

  while True:
    data = ser.readline()
    if data:
      str = data.decode('unicode_escape').strip("\r").strip("\n")
      tm = datetime.now().time()
      if sc.is_ack(str) == True:
          print("{} {}".format(tm, "ack"))
      elif sc.is_nack(str) == True:
          print("{} {}".format(tm, "nack"))
      elif len(str) > 0 and str[0] in ['t', 'T', 'r', 'R']:
        print("{} {}".format(tm, sc.format_from_slcan(str)))
      else:
        print("{} {}".format(tm, str))

    curr_secs = time.time()
    for c in can_msgs:
      if "count" in c and c["count"] == 0:
        continue
      if curr_secs - c["prev_secs"] > c["interval"]:
        msg = c["can_msg"]
        su.send_can_frame(ser, msg["id"], msg["data"], msg["is_ext"])
        c["prev_secs"] = curr_secs
        if "count" in c:
          c["count"] -= 1
        print("{} SENT: {} {}".format(datetime.now().time(), curr_secs, msg))

if __name__ == '__main__':

  parser = argparse.ArgumentParser()
  parser.add_argument("port", help = "Serial Port (required)")
  parser.add_argument("-b", "--baud", help = "BAUD Rate (default 115200)")
  
  # TODO: add option whether to log incoming or not, default yes
  args = parser.parse_args()

  if not args.port:
    print("Please specify port to listen to. Exiting ....")
    exit

  baud = 115200
  if args.baud:
    baud = args.baud

  run(port=args.port, baud=baud)
