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
Note, this is from the original repo, and not tested at the initial commit time.

#### Environments
Install SocketCAN
```
    sudo apt install can-utils
```

Please replace ttyUSB with ttyACM in case of using Arduino Uno.
```
    # Setup
    sudo slcan_attach -f -s6 -o /dev/ttyUSB0  
    sudo slcand -S 1000000 ttyUSB0 can0  
    sudo ifconfig can0 up  

    # To monitor
    candump can0
    
    # Cleanup
    sudo ifconfig can0 down  
    sudo killall slcand  
```