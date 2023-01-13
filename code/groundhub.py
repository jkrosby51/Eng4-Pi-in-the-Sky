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

#LoRa setup

# Define radio parameters.
RADIO_FREQ_MHZ = 915.0  # Frequency of the radio in Mhz. Must match your
# module! Can be a value like 915.0, 433.0, etc.

# Define pins connected to the chip, use these if wiring up the breakout according to the guide:
CS = digitalio.DigitalInOut(board.D5)
RESET = digitalio.DigitalInOut(board.D6)
# Or uncomment and instead use these if using a Feather M0 RFM9x board and the appropriate
# CircuitPython build:
# CS = digitalio.DigitalInOut(board.RFM9X_CS)
# RESET = digitalio.DigitalInOut(board.RFM9X_RST)

# Initialize SPI bus.
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

# Initialze RFM radio
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, RADIO_FREQ_MHZ)

# Note that the radio is configured in LoRa mode so you can't control sync
# word, encryption, frequency deviation, or other settings!

# You can however adjust the transmit power (in dB).  The default is 13 dB but
# high power radios like the RFM95 can go up to 23 dB:
rfm9x.tx_power = 23

#other setup

sda_pin = board.GP14        #UPDATE AS NEEDED
scl_pin = board.GP15        #UPDATE AS NEEDED
i2c = busio.I2C(scl_pin, sda_pin)
sensor = adafruit_mpl3115a2.MPL3115A2(i2c)


sealevel_Pa = 102290                           ### Find current sea level kPa in Charlottesville here: https://barometricpressure.app/results?lat=38.0386569&lng=-78.4846401
sensor.sealevel_pressure =  sealevel_Pa         ### Manually set sealevel pressure (in Pascals) based on current weather data for more accuracy
altitude_initial = 0 #sets initial altitude
max_altitude = 22 #temporary value

msg1 = ["helloo!", "n"] # turret_autosearch_1
msg2 = ["put me down!", "n"] # turret_pickup_2
msg3 = ["who are you?", "n"] # turret_pickup_5
msg4 = ["help", "n"] # turret _pickup_8
msg5 = ["are you still there?", "n"] # turret_search_1
msg6 = ["no hard feelings", "n"] # turret_disabled_8
msg7 = ["whyyyy", "n"] # turret_disabled_7
msg8 = ["i dont blame you", "n"] # turret_disabled_5
msg9 = ["my fault", 'n'] # turret_collide_4
msg10 = ["goodnight", "n"] # turret_retire_5
msg11 = ["aaaaaaaaa", "n"] #turret_fizzler_1

'''`
other potential voice lines:
- turret_tipped_5
- sp_sabotage_factory_good_fail02
- sp_sabotage_factory_good_fail03
- sp_sabotage_factory_good_fail05
- sp_sabotage_factory_good_fail06
- turretlaunched01
- turretlaunched02
- turretlaunched03
- turretlaunched05
- turretlaunched06
- turretlaunched07
- turretlaunched10
- turretlightbridgeblock02
- turretlightbridgeblock03
- turretshotbylaser07
- turretshotbylaser08
- turretstuckintubetakemewith01
- turretstuckintubegoodbye01
- turretstuckintubetakemewith02
- turretwitnessdeath11
- turret_tipped_6
- turretstuckintube09
- turret_autosearch_1
- turret_pickup_2
- turret_pickup_5
- turret_pickup_8
- turret_search_1
- turret_disabled_8
- turret_disabled_7
- turret_disabled_5
- turret_collide_4
- turret_retire_5
- turret_fizzler_1
- turretlaunched09
- turretlaunched08
- sp_sabotage_factory_good_fail04

'''
#see also "weeeeee - OHNO" "Im flying!" for message 11

print("Waiting for packets...")

while True:
    packet = rfm9x.receive()
    # Optionally change the receive timeout from its default of 0.5 seconds:
    # packet = rfm9x.receive(timeout=5.0)
    # If no packet was received during the timeout then None is returned.
    if packet is None:
        # Packet has not been received
        LED.value = False
        print("Received nothing! Listening again...")
    else:
        # Received a packet!
        LED.value = True
        # Print out the raw bytes of the packet:
        print("Received (raw bytes): {0}".format(packet))
        # And decode to ASCII text and print it too.  Note that you always
        # receive raw bytes and need to convert to a text format like ASCII
        # if you intend to do string processing on your data.  Make sure the
        # sending side is sending ASCII data before you try to decode!
        packet_text = str(packet, "ascii")
        print("Received (ASCII): {0}".format(packet_text))
        # Also read the RSSI (signal strength) of the last received message and
        # print it.
        rssi = rfm9x.last_rssi
        print("Received signal strength: {0} dB".format(rssi))

    current_altitude = int(packet_text)
    
    print(f"Altitude: {current_altitude} meters")
    
    
    if altitude_initial = 0:
        altitude_intial = current_altitude
    
    if (current_altitude - altitude_initial) > 0 and (current_altitude - altitude_initial) < 2 and msg1[1] == "n": #temporary altitude values
        print(msg1[0])
        msg1[1] = "y"
        
    if (current_altitude - altitude_initial) > 2 and (current_altitude - altitude_initial) < 4 and msg2[1] == "n": #temporary altitude values
        print(msg2[0])
        msg2[1] = "y"
        
    if (current_altitude - altitude_initial) > 4 and (current_altitude - altitude_initial) < 6 and msg3[1] == "n": #temporary altitude values
        print(msg3[0])
        msg3[1] = "y"
        
    if (current_altitude - altitude_initial) > 6 and (current_altitude - altitude_initial) < 8 and msg4[1] == "n": #temporary altitude values
        print(msg4[0])
        msg4[1] = "y"
        
    if (current_altitude - altitude_initial) > 8 and (current_altitude - altitude_initial) < 10 and msg5[1] == "n": #temporary altitude values
        print(msg5[0])
        msg5[1] = "y"
        
    if (current_altitude - altitude_initial) > 10 and (current_altitude - altitude_initial) < 12 and msg6[1] == "n": #temporary altitude values
        print(msg6[0])
        msg6[1] = "y"
        
    if (current_altitude - altitude_initial) > 12 and (current_altitude - altitude_initial) < 14 and msg7[1] == "n": #temporary altitude values
        print(msg7[0])
        msg7[1] = "y"
        
    if (current_altitude - altitude_initial) > 14 and (current_altitude - altitude_initial) < 16 and msg8[1] == "n": #temporary altitude values
        print(msg8[0])
        msg8[1] = "y"
        
    if (current_altitude - altitude_initial) > 16 and (current_altitude - altitude_initial) < 18 and msg9[1] == "n": #temporary altitude values
        print(msg9[0])
        msg9[1] = "y"
        
    if (current_altitude - altitude_initial) > 18 and (current_altitude - altitude_initial) < 20 and msg10[1] == "n": #temporary altitude values
        print(msg10[0])
        msg10[1] = "y"
    