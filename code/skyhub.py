#type: ignore
# https://learn.adafruit.com/using-mpl3115a2-with-circuitpython
# https://www.tomshardware.com/how-to/get-wi-fi-internet-on-raspberry-pi-pico
# https://www.howtoforge.com/using-an-android-smartphone-as-a-wlan-hotspot

import math
import time

import adafruit_mpl3115a2
import adafruit_rfm9x
import board
import busio
import digitalio
import pwmio
from adafruit_motor import servo
import microcontroller

sda_pin = board.GP0   
scl_pin = board.GP1      
i2c = busio.I2C(scl_pin, sda_pin)
sensor = adafruit_mpl3115a2.MPL3115A2(i2c)

RADIO_FREQ_MHZ = 915.0
CS = digitalio.DigitalInOut(board.GP7)
RESET = digitalio.DigitalInOut(board.GP6)
spi = busio.SPI(clock=board.GP2, MOSI=board.GP3, MISO=board.GP4)
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, RADIO_FREQ_MHZ)
rfm9x.tx_power = 23

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

altitude_initial = sensor.altitude #sets initial altitude to be starting altitude instead of sea-level

#If opened in data logging mode, log all data as it's collected and sent. Otherwise only collect and send.
try:
    with open("/boot_out.txt", "a") as datalogger:
        led.value = True
        datalogger.write("-------------------------")
        while True:
            alt = sensor.altitude - altitude_initial + 1
            print(alt)
            rfm9x.send(str(alt))
            
            datalogger.write(f"{alt}\n")
            datalogger.flush()
            time.sleep(.2)
except OSError as e:  # Typically when the filesystem isn't writeable...
    led.value = False
    while True:
        alt = sensor.altitude - altitude_initial + 1
        print(alt)
        rfm9x.send(str(alt))
    
