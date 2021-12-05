# Slcanuino PIO

Transmit and receive CAN messages from/to your computer (MacOS/Windows/Linux) via USB to CAN H/L bus. This is a fork of [kahiroka/slcanuino](https://github.com/kahiroka/slcanuino), with these changes:
- using platformio project
- control from plain python (runnable from e.g. MacOS)

Please read the original README file for more information.

## Bill of Materials
This repo was deployed and tested on these:
- Arduino Nano
- Seeed Studio CAN-BUS Shield V1.2
- Computer: MacOS

For the example scripts
- Python: 3.9.7 (todo: list libraries like pyserial)

## Connections
- CAN-BUS Shield: mount to Arduino Uno
- GREEN LED (for OK sign): pin 5 (analog)
- RED LED (for ERROR sign): pin 6 (analog)

## Usage
After flashing

### MacOS
1. Connect to USB, get the device name (e.g. ```/dev/cu.usbmodem000``` - somehow it labels Arduino as usbmodem)
2. Run the controller python script
```
    # activate virtual env, do the pip install for the first time
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

    # run the script, specifying your device
    python3 runner.py -b 115200 /dev/cu.usbmodem000
```
3. By default the script prints incoming message to stdout and periodically send preset CAN messages. Alter the script to your heart's content. 

### Linux
Tested on Raspberry Pi.

#### Environments
Install SocketCAN
```
    $ udo apt install can-utils
```

Check exact string of ttyACM (in case of using Arduino Uno) under ```/dev/```
```
    # Setups
    $ sudo slcan_attach -f -s6 -o /dev/ttyACM0
        attached tty /dev/ttyACM0 to netdevice slcan0
    $ sudo slcand -S 115200 ttyACM0 slcan0
    $ sudo ip link set up slcan0

    # Check setups
    $ ip addr | grep slcan0
        5: slcan0: <NOARP,UP,LOWER_UP> mtu 16 qdisc pfifo_fast state UNKNOWN group default qlen 10

    # Actions
    $ candump slcan0
    $ cansend slcan0 333#babefeedbabefeed
    $ cansend slcan0 1234DCBA#babefeedcafedead

    # Cleanups
    $ sudo ifconfig slcan0 down
    $ sudo killall slcand
```