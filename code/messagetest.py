#type: ignore
# https://learn.adafruit.com/using-mpl3115a2-with-circuitpython
# https://www.tomshardware.com/how-to/get-wi-fi-internet-on-raspberry-pi-pico
# https://www.howtoforge.com/using-an-android-smartphone-as-a-wlan-hotspot
'''
LoRa code:
    SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
    SPDX-License-Identifier: MIT
    Author: Tony DiCola
    Link: https://learn.adafruit.com/adafruit-rfm69hcw-and-rfm96-rfm95-rfm98-lora-packet-padio-breakouts/circuitpython-for-rfm9x-lora
'''

import math
import time

import adafruit_mpl3115a2
import adafruit_rfm9x
import board
import busio
import digitalio
import pwmio
from adafruit_display_shapes.triangle import Triangle
from adafruit_display_shapes.line import Line
from adafruit_display_shapes.circle import Circle
import busio
import displayio
import terminalio
import adafruit_displayio_ssd1306
from adafruit_display_text import label
displayio.release_displays() #set up for OLED screen

sda_pin = board.GP14 #sets pin for sda
scl_pin = board.GP15 #sets pin for scl
i2c = busio.I2C(scl_pin, sda_pin) #sets i2c

display_bus = displayio.I2CDisplay(i2c, device_address = 0x3d, reset = board.GP2) #sets up OLED screen
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=64) #sets up OLED screen


#LoRa setup

# Define radio parameters.
RADIO_FREQ_MHZ = 915.0  # Frequency of the radio in Mhz. Must match yourm module!

# Define pins connected to the chip, use these if wiring up the breakout according to the guide:
CS = digitalio.DigitalInOut(board.GP17)
RESET = digitalio.DigitalInOut(board.GP16)

# Initialize SPI bus.
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

# Initialze RFM radio
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, RADIO_FREQ_MHZ)

# Note that the radio is configured in LoRa mode so you can't control sync word, encryption, frequency deviation, or other settings!
# You can however adjust the transmit power (in dB).  The default is 13 dB butm high power radios like the RFM95 can go up to 23 dB:

rfm9x.tx_power = 23

lastMeters = 0 #sets last known altitude to 0
currentMeters = 0 #sets initial current altitude to 0
max_altitude = 22 #temporary value

max_area = 100  
mid_x = 64 #x-coordinate of center of OLED screen display
mid_y = 32 #y-coordinate of center of OLED screen display
min_distance = 10000000000

start_time = time.monotonic()
altlist = [0] #creates list of altitudes
timelist = [0] #creates list of times
     
messagePin = #array full of pins! wait- is that a real thing?

print("Waiting for packets...")


while True:
    packet = rfm9x.receive()

    # If no packet was received during the timeout then None is returned.
    if packet is None:
        # Packet has not been received
        LED.value = False
        print("Received nothing! Listening again...")
    else:
        # Received a packet!
        LED.value = True
        # Print out the raw bytes of the packet:
        print("Received (raw bytes): {0}".format(packet)) # decodes to ASCII text and prints it
        # raw bytes are always recieved, must be converted to text format like ASCII to do string processing on data. 
        # always make sure ASCII data is being sent before trying to decode
        
        packet_text = str(packet, "ascii")
        print("Received (ASCII): {0}".format(packet_text)) #reads the RSSI (signal strength) of last recieved message and prints it

        rssi = rfm9x.last_rssi
        print("Received signal strength: {0} dB".format(rssi))

    currentMeters = int(packet_text)
    
    print(f"Altitude: {current_altitude} meters")
    if currentMeters - lastMeters >= 3:
        currentPin = digitalio.DigitalInOut(messagePin[currentMeters])
        currentPin.direction = digitalio.Direction.OUTPUT
        currentPin = True #or is it false?? idk
        time.sleep(.5)
        currentPin = False
        altlist.append(currentMeters)
        timelist.append(time.monotonic() - start_time)
        lastMeters = currentMeters
        
    

    splash = displayio.Group() #creates display group
    
    hline = Line(0,5,128,5, color=0xFFFF00) #sets color, start coordinates, and end coordinates of the line serving as the x-axis
    splash.append(hline) #adds to splash
        
    vline = Line(5,64,5,0, color=0xFFFF00) #sets color, start coordinates, and end coordinates of the line serving as the y-axis
    splash.append(vline) #adds to splash
        
    display.show(splash) #sends display group to OLED screen

    time.sleep(1) #wait one second