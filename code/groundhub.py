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

import time

import adafruit_ili9341
import adafruit_rfm9x
import board
import busio
import digitalio
import displayio
import terminalio
from adafruit_display_shapes.line import Line
from adafruit_display_shapes.rect import Rect
from adafruit_display_text import label

displayio.release_displays() #set up for screen by releasing all used pins for new display

spi = busio.SPI(clock=board.D13, MOSI=board.D11, MISO=board.D12)

tft_cs = board.D10
tft_dc = board.D9

display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs)
display = adafruit_ili9341.ILI9341(display_bus, width=320, height=240, rotation=180) #the last variable rotates the screen 180°, since the CAD element attaches the screen upsidedown

# Make the display context
splash = displayio.Group()
display.show(splash)

# Draw a background
color_bitmap = displayio.Bitmap(320, 240, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0xC3AFDB #Light Purple

bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)

splash.append(bg_sprite)

# Make the graph's axes
hRect = Rect(40, 200, 240, 2, fill=0x470400)#sets start coordinates, width, height, and fill color of the line serving as the x-axis
splash.append(hRect) #adds to splash

vRect = Rect(40, 40, 2, 160, fill=0x470400) #sets start coordinates, width, height, and fill color of the line serving as the y-axis
splash.append(vRect) #adds to splash

### My science teacher said we have to label the axes!!!!! pls add >:(

#label the x-axis
text_group = displayio.Group(scale=1, x=240, y=210) #sets size and start position of message
text = "time(s)"
text_area = label.Label(terminalio.FONT, text=text, color=0x470400) #adds text to label x-axis to display group
text_group.append(text_area)  #subgroup for text scaling
splash.append(text_group) #adds to splash

#label the y-axis
text_group = displayio.Group(scale=1, x=3, y=45) #sets size and start position of message
text = "alt(m)"
text_area = label.Label(terminalio.FONT, text=text, color=0x470400) #adds text to label y-axis to display group
text_group.append(text_area)  #subgroup for text scaling
splash.append(text_group) #adds to splash

yPixel = 160 #origin of graph
xPixel = 40 #origin of graph

#sets pins as the right direction n all that and then shoves em into a cool array for future use!
msgPins = []
pinArr = [board.A5, board.A4, board.D5, board.D6, board.D7, board.D8, board.A3, board.A2]
for i in range(0, len(pinArr) ):
    tempPin = digitalio.DigitalInOut(pinArr[i])
    tempPin.direction = digitalio.Direction.OUTPUT
    tempPin.value = False
    msgPins.append(tempPin)  

#LoRa setup

# Define radio parameters.
RADIO_FREQ_MHZ = 915.0 # Frequency of the radio in Mhz. Must match yourm module!

# Define pins connected to the chip, use these if wiring up the breakout according to the guide:
LoRa_CS = digitalio.DigitalInOut(board.D3)
LoRa_RESET = digitalio.DigitalInOut(board.D4)
# Initialze RFM radio
rfm9x = adafruit_rfm9x.RFM9x(spi, LoRa_CS, LoRa_RESET, RADIO_FREQ_MHZ)

# Note that the radio is configured in LoRa mode so you can't control sync word, encryption, frequency deviation, or other settings!
# You can however adjust the transmit power (in dB). The default is 13 dB butm high power radios like the RFM95 can go up to 23 dB:

rfm9x.tx_power = 23

lastMeters = 0 #sets last known altitude to 0
currentMeters = 0 #sets initial current altitude to 0
max_altitude = 22 #temporary value

max_area = 100
min_distance = 10000000000

start_time = time.monotonic()
altlist = [0] #creates list of altitudes
timelist = [0] #creates list of times


print("Waiting for packets...")

#sets pins as the right direction n all that and then shoves em into a cool array for future use!
msgPins = []
pinArr = [board.A5, board.A4, board.D5, board.D6, board.D7, board.D8, board.A3, board.A2]
for i in range(0, len(pinArr) ):
    tempPin = digitalio.DigitalInOut(pinArr[i])
    tempPin.direction = digitalio.Direction.OUTPUT
    tempPin.value = False
    msgPins.append(tempPin)  

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
        #takes pin from already setup array of pins, sets it on and off to simulate a button press to the board
        msgPins[int(int(currentMeters) / 3)].value = True #or is it False??  
        time.sleep(.2)
        msgPins[int(int(currentMeters) / 3)].value = False #or is it True?? 

        altlist.append(currentMeters)
        timelist.append(time.monotonic() - start_time)
        lastMeters = currentMeters


    for i in range(len(timelist)-1): #is that syntax correct for range()? -------------------------CHECK

        line = Line(xPixel+timelist[i], yPixel-altlist[i], xPixel+timelist[i+1], yPixel-altlist[i+1], color=0xFFFF00)
        splash.append(line)



    #display.show(splash) #sends display group to OLED screen

    time.sleep(1) #wait one second
