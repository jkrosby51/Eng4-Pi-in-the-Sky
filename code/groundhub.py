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
from adafruit_display_shapes.circle import Circle
from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font

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

#makes a custom font to use for the coordinate labels
coord_font = bitmap_font.load_font("/lib/JosefinSans-Bold-10.bdf")

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

#LoRa setup

# Define radio parameters.
RADIO_FREQ_MHZ = 915.0 # Frequency of the radio in Mhz. Must match yourm module!

# Define pins connected to the chip, use these if wiring up the breakout according to the guide:
LoRa_CS = digitalio.DigitalInOut(board.D3)
LoRa_RESET = digitalio.DigitalInOut(board.D5)
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

#list of messages to use when going up
upmessage_array = ["Hellooo!", "Put me down!", "What are you doing?", "Help!", "Thanks anyway...", "I'm scared..."]

#list of messages to use when going down
downmessage_array = ["AHHHHHHHHH!", "I'm flyinnnng!"]

message_text = displayio.Group(scale=2, x=5, y=220) #sets size and start position of message
msg = upmessage_array[0] #chooses the appropriate message from the array and sets it as the text
msg_area = label.Label(terminalio.FONT, text=msg, color=0x470400) #adds text to label y-axis to display group
message_text.append(msg_area)  #subgroup for text scaling
splash.append(message_text) #adds to splash

descending = False #creates a variable that tells us whether the payload is ascending or descending; starts as False to indicate ascending

print("Waiting for packets...")

while True:
    packet = rfm9x.receive()

    # If no packet was received during the timeout then None is returned.
    if packet is None:
        # Packet has not been received
        print("Received nothing! Listening again...")
    else:
        # Received a packet!
        # Print out the raw bytes of the packet:
        print("Received (raw bytes): {0}".format(packet)) # decodes to ASCII text and prints it
        # raw bytes are always recieved, must be converted to text format like ASCII to do string processing on data.
        # always make sure ASCII data is being sent before trying to decode

        packet_text = str(packet, "ascii")
        print("Received (ASCII): {0}".format(packet_text)) #reads the RSSI (signal strength) of last recieved message and prints it

        rssi = rfm9x.last_rssi
        print("Received signal strength: {0} dB".format(rssi))

        currentMeters = int(float(packet_text))

        print(f"Altitude: {currentMeters} meters")
        
        if currentMeters >= 7:
            descending = True #changes value of "descending" to indicate that the payload is now descending; only happens once it reaches its maximum altitude of seven meters
            
        #Compares the current altitude value recieved by the LoRa with the last graphed altitude (note! the last graphed altitude is not the same as the last recieved altitude!) 
        #If this value is greater than or equal to 1 and the payload is ascending, continue
        if (currentMeters - lastMeters) >= 1 and descending == False:
            msg_area.msg = upmessage_array[int(currentMeters/3)] #changes the message text displayed to appropriate one from array
            
            altlist.append(currentMeters) #adds the current altitude to altlist
            timelist.append(int(time.monotonic() - start_time)) #finds the current time elapsed by subtracting time.monotonic from the start time, and adds it to timelist
            lastMeters = currentMeters #sets lastMeters equal to currentMeters, making it the new last graphed time
        
        #Only do this if the payload is descending! The distance between lastMeters and currentMeters is not needed here
        if descending == True:
            msg_area.msg = downmessage_array[0] #changes the message text displayed to appropriate one from array
            time.sleep(2) #waits two seconds
            msg_area.msg = downmessage_array[1] #changes the message text displayed to appropriate one from array
            
            altlist.append(currentMeters)  #adds the current altitude to altlist
            timelist.append(int(time.monotonic() - start_time)) #finds the current time elapsed by subtracting time.monotonic from the start time, and adds it to timelist
            lastMeters = currentMeters #sets lastMeters equal to currentMeters, making it the new last graphed time
            
        if currentMeters != lastMeters:
            #creates line to display data! First two parameters are the initial x- and y-positions of the line, and the second two are the final x- and y-positions! The final paramter sets the color of the line
            #timelist[len(timelist)-2] ensures that the new line starts at the x-coordinate of the last point, and altlist[len(altlist-2)] ensures that the new line starts at the y-coordinate of the last point
            #any time a part of timelist is called, it must be added to xPixel in order to create the line with respect to the origin of the graph, and whenever a part of altlist is called, it must be subtracted from yPixel for the same reason
            #The second pair of x- and y-coordinates are written with timelist[i+1] and altlist[i+1] respectively to ensure that the line will end at the next data point
            #timelist is multiplied by 3 and altlist is multiplied by 18 in order to scale the graph to be visible and large enough to distinguish individual data points
            line = Line((xPixel+3*timelist[len(timelist)-2]), (yPixel-18*altlist[len(altlist)-2]), (xPixel+3*timelist[len(timelist)-1]), (yPixel-18*altlist[len(timelist)-1]), color=0xff5d00)
            splash.append(line)

            #The first two parameters center the circle around the data point at the end of the last graphed line
            circle = Circle(xPixel+3*(timelist[len(timelist)-1]), yPixel-18*(altlist[len(altlist)-1]), 2, fill=0x0065ff, outline=0x0065ff)
            splash.append(circle)
            point_label = displayio.Group(scale=1, x=(xPixel+timelist[len(timelist)-1]-10), y=(yPixel-18*(altlist[len(altlist)-1])-8)) #sets font, size, and start position of message
            point = f"({timelist[len(timelist)-1]}, {altlist[len(timelist)-1]})" #makes an f-string with showing the coordinates; these coordinates are defined by the last thing in timelist and altlist
            text_area = label.Label(coord_font, text=point, color=0x470400) #adds coordinate text to display group
            point_label.append(text_area)  #subgroup for text scaling
            splash.append(point_label) #adds to splash
        
        if len(altlist) > 8:
            break #breaks out of the else statement to stop graphing and avoid memory error after collecting the desired number of data points

